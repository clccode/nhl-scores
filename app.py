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
    col, _ = st.columns([1, 2])
    with col:
        st.subheader("Goals Leaders")
        st.dataframe(get_leaders("goals", "Goals"), use_container_width=False)
        st.divider()
        st.subheader("Assists Leaders")
        st.dataframe(get_leaders("assists", "Assists"), use_container_width=False)
        st.divider()
        st.subheader("Points Leaders")
        st.dataframe(get_leaders("points", "Points"), use_container_width=False)
        st.divider()
        st.subheader("Plus/Minus Leaders")
        st.dataframe(get_leaders("plusMinus", "+/-"), use_container_width=False)
        st.divider()
        st.subheader("Penalty Minutes Leaders")
        st.dataframe(get_leaders("penaltyMins", "PIM"), use_container_width=False)