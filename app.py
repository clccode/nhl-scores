import streamlit as st
from datetime import datetime
from nhl_scores import get_period_label, display_goals, get_scores
from nhl_standings import display_standings_page

st.set_page_config(page_title="NHL Scores & Standings", page_icon="🏒", layout="wide")

# add sidebar with date input
st.sidebar.header("Select Date")
selected_date = st.sidebar.date_input("Select a date", datetime.now()) 
if st.sidebar.button("🔄 Refresh Scores 🔄"):
    st.rerun() 

scores_tab, standings_tab = st.tabs(["Scores", "Standings"])

with scores_tab:
    st.title(f"🏒 NHL Scores - {selected_date.strftime('%B %-d, %Y')}")
    get_scores(selected_date.strftime('%Y-%m-%d'))

with standings_tab:
    st.title(f"📋 NHL Standings - {selected_date.strftime('%B %-d, %Y')}")
    display_standings_page(selected_date.strftime('%Y-%m-%d')) 