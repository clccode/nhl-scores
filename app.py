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
    st.title("🌟 NHL Leaders")
    col, _ = st.columns([1, 2])
    with col:
        st.header("Skater Leaders")
        st.subheader("Goals")
        st.dataframe(get_leaders("goals", "skater", "Goals"), use_container_width=False)
        st.divider()
        st.subheader("Assists")
        st.dataframe(get_leaders("assists", "skater", "Assists"), use_container_width=False)
        st.divider()
        st.subheader("Points")
        st.dataframe(get_leaders("points", "skater", "Points"), use_container_width=False)
        st.divider()
        st.subheader("Plus/Minus")
        st.dataframe(get_leaders("plusMinus", "skater", "+/-"), use_container_width=False)
        st.divider()
        st.subheader("Penalty Minutes")
        st.dataframe(get_leaders("penaltyMins", "skater", "PIM"), use_container_width=False)
        st.divider()
        st.header("Goalie Leaders")
        st.subheader("Wins")
        st.dataframe(get_leaders("wins", "goalie", "Wins"), use_container_width=False)
        st.divider()
        st.subheader("Goals Against Average")
        st.dataframe(get_leaders("goalsAgainstAverage", "goalie", "GAA"), use_container_width=False)
        st.divider()
        st.subheader("Save Percentage")
        st.dataframe(get_leaders("savePctg", "goalie", "SV%"), use_container_width=False)