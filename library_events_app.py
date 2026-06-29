import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Library Events MA", layout="wide")
st.title("📅 Minuteman + BPL Library Events Aggregator")
st.markdown("Day-wise events from Minuteman branches & Boston Public Library. Month calendar search.")

# Sidebar filters
st.sidebar.header("Filters")
selected_month = st.sidebar.date_input("Select Month Start", datetime.now())
branch_filter = st.sidebar.text_input("Filter by Branch (e.g., Hyde Park, Central)", "")

st.subheader(f"Events around {selected_month.strftime('%B %Y')}")

# Placeholder data (replace with scraper/API later)
data = [
    {"Date": "2026-06-29", "Branch": "Jamaica Plain (BPL)", "Event": "Memory Café", "Time": "10:30am-12pm", "Link": "https://bpl.bibliocommons.com/events/"},
    {"Date": "2026-06-29", "Branch": "Hyde Park (BPL)", "Event": "Basketry Workshop", "Time": "10:30am", "Link": "https://bpl.bibliocommons.com/events/"},
    # Add more from Minuteman/BPL calendars
    {"Date": "2026-06-30", "Branch": "Various Minuteman", "Event": "Branch Programs", "Time": "Check site", "Link": "https://www.minlib.net/calendar"},
]

df = pd.DataFrame(data)
if branch_filter:
    df = df[df['Branch'].str.contains(branch_filter, case=False)]

st.dataframe(df, use_container_width=True)

if st.button("🔄 Refresh Events (Demo)"):
    st.success("In full version: Scrapes minlib.net/calendar + bpl.bibliocommons.com/events for selected month/day.")
    st.info("Tip: Many BPL story times daily; Minuteman via branch LibCal.")

st.caption("Data collected from official calendars. For production, add BeautifulSoup/Selenium.")
