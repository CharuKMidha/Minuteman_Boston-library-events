import streamlit as st
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

st.set_page_config(page_title="Library Events MA", layout="wide")
st.title("📅 Live Minuteman + BPL Events (Selenium Scraper)")

st.sidebar.header("Filters")
selected_date = st.sidebar.date_input("Select Date", datetime.now())

# Full Branch Lists
bpl_branches = ["All BPL", "Central Library in Copley Square", "Hyde Park", "Jamaica Plain", "North End", "South Boston", 
                "Mattapan", "Chinatown", "West End", "Grove Hall", "Adams Street", "Brighton", "Charlestown", 
                "Codman Square", "Connolly", "East Boston", "Fields Corner", "Roslindale", "Roxbury", "Shaw-Roxbury"]

minuteman_branches = ["All Minuteman", "Acton", "Arlington", "Ashland", "Bedford", "Belmont", "Brookline", "Cambridge", 
                      "Concord", "Dedham", "Dover", "Framingham", "Lexington", "Lincoln", "Natick", "Needham", 
                      "Newton", "Sudbury", "Waltham", "Watertown", "Wayland", "Weston", "Winchester", "Woburn"]

all_branches = ["All Branches"] + [b for b in bpl_branches[1:]] + [m for m in minuteman_branches[1:]]
selected_branch = st.sidebar.selectbox("Select Branch", all_branches)

@st.cache_data(ttl=1800)  # Cache 30 min
def scrape_with_selenium(url, wait_time=10):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(wait_time)  # Wait for JS load
        
        # Example extraction (customize selectors per site)
        events = []
        # For BPL - look for event cards
        try:
            event_elements = driver.find_elements(By.CSS_SELECTOR, "div.event-item, .event, a[href*='events']")  # Adjust selectors
            for el in event_elements[:10]:  # Limit
                text = el.text.strip()
                if text:
                    events.append({"Event": text[:100], "Branch": "BPL", "Time": "See details", "Source": "BPL"})
        except:
            pass
        
        driver.quit()
        return pd.DataFrame(events) if events else pd.DataFrame([{"Event": "No events extracted", "Branch": "Various", "Time": "Try again"}])
    except Exception as e:
        return pd.DataFrame([{"Event": f"Error: {str(e)[:100]}", "Branch": "N/A", "Time": "Check deployment"}])

# Fetch
bpl_url = "https://bpl.bibliocommons.com/events/"
min_url = "https://www.minlib.net/calendar"

bpl_df = scrape_with_selenium(bpl_url)
min_df = scrape_with_selenium(min_url)

combined_df = pd.concat([bpl_df, min_df], ignore_index=True)

# Apply filters
if selected_branch != "All Branches":
    combined_df = combined_df[combined_df.get('Branch', '').str.contains(selected_branch.split()[0], case=False, na=False)]

st.subheader(f"Events for {selected_date.strftime('%B %d, %Y')}")
if combined_df.empty or combined_df.iloc[0]['Event'].startswith("Error"):
    st.warning("Scraping may be limited in Streamlit Cloud (headless env). Test locally or improve selectors.")
else:
    st.dataframe(combined_df, use_container_width=True)

if st.button("🔄 Refresh Live Scrape"):
    st.cache_data.clear()
    st.rerun()

st.caption("Selenium handles JS calendars. Improve CSS selectors for better extraction. Full branches supported.")
