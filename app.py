import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from nhl_scores import get_scores
from nhl_standings import display_standings_page
from nhl_leaders import get_leaders

st.set_page_config(page_title="NHL Scores & Standings", page_icon="🏒", layout="wide")

# add sidebar with date input
st.sidebar.header("Select Date")
selected_date = st.sidebar.date_input("Select a date",  datetime.now(ZoneInfo('US/Eastern'))  ) 
if st.sidebar.button("🔄 Refresh Scores 🔄"):
    st.rerun() 

scores_tab, standings_tab, leaders_tab = st.tabs(["Scores", "Standings", "Leaders"])

with scores_tab:
    st.title(f"🏒 NHL Scores - {selected_date.strftime('%B %-d, %Y')}")
    get_scores(selected_date.strftime('%Y-%m-%d'))

with standings_tab:
    st.title(f"📋 NHL Standings - {selected_date.strftime('%B %-d, %Y')}")
    display_standings_page(selected_date.strftime('%Y-%m-%d')) 

with leaders_tab:
    st.title(f"🌟 NHL Leaders - {selected_date.strftime('%B %-d, %Y')}")
    st.subheader("Goals Leaders")
    get_leaders("goals", "Goals")
    st.subheader("Assists Leaders")
    get_leaders("assists", "Assists")
    st.subheader("Points Leaders")
    get_leaders("points", "Points")
    st.subheader("Plus/Minus Leaders")
    get_leaders("plusMinus", "+/-")
    st.subheader("Penalty Minutes Leaders")
    get_leaders("penaltyMins", "PIM")