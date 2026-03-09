import streamlit as st
import pandas as pd
import requests

@st.cache_data(ttl=300) # cache for 300 seconds (5 minutes)
def get_standings(date):
    url = f"https://api-web.nhle.com/v1/standings/{date}"
    response = requests.get(url)
    data = response.json()
    return data['standings']  # return the raw API data

# set up the function to retrieve the standings
def build_standings_df(teams):
    rows = []
    for team in teams:
        rows.append({
            'Team': team['teamAbbrev']['default'],
            'GP': team['gamesPlayed'],
            'W': team['wins'],
            'L': team['losses'],
            'OT': team['otLosses'],
            'PTS': team['points'],
            'P%': f"{team['pointPctg']:.3f}"[1:],
            'RW': team['regulationWins'],
            'ROW': team['regulationPlusOtWins'],
            'GF': team['goalFor'],
            'GA': team['goalAgainst'],
            'DIFF': f"+{team['goalDifferential']}" if team['goalDifferential'] > 0 else str(team['goalDifferential']),
            'HOME': f"{team['homeWins']}-{team['homeLosses']}-{team['homeOtLosses']}",
            'AWAY': f"{team['roadWins']}-{team['roadLosses']}-{team['roadOtLosses']}",
            'S/O': f"{team['shootoutWins']}-{team['shootoutLosses']}",
            'L10': f"{team['l10Wins']}-{team['l10Losses']}-{team['l10OtLosses']}",
            'STRK': f"{team['streakCode']}{team['streakCount']}"
        })
    df = pd.DataFrame(rows)
    df.index = range(1, len(df) + 1)
    df.index.name = "Rank"
    return df

# style the goal differential columns for teams with positive and negative gd
# def style_diff(val):
#     if isinstance(val, str) and val.startswith('+'):
#         return 'color: #34d399'
#     elif isinstance(val, str) and val.startswith('-'):
#         return 'color: #f87171'
#     return ''

# display wildcard dataframe with a line under the top 2 teams
def display_standings(df, show_cutoff=True):
    html = '<table style="width:100%; border-collapse:collapse; font-size:0.85rem;">'

    # header row
    html += '<tr>'
    html += '<th style="padding:6px 8px; text-align:left;">Rank</th>'
    for col in df.columns:
        html += f'<th style="padding:6px 8px; text-align:right; border-bottom:1px solid #444;">{col}</th>'
    html += '</tr>'

    # data rows
    for i, (idx, row) in enumerate(df.iterrows()):
        border = 'border-bottom: 2px solid #ef4444;' if (show_cutoff and i == 1) else ''
        html += f'<tr style="{border}">'
        html += f'<td style="padding:6px 8px; text-align:left;">{idx}</td>'
        for col in df.columns:
            val = row[col]
            style = 'padding:6px 8px; text-align:right;'
            if col == 'DIFF' and isinstance(val, str):
                if val.startswith('+'):
                    style += ' color:#34d399;'
                elif val.startswith('-'):
                    style += ' color:#f87171;'
            if col == 'Team': style = style.replace('right', 'left')
            html += f'<td style="{style}">{val}</td>'
        html += '</tr>'

    html += '</table>'
    st.markdown(html, unsafe_allow_html=True)

# function to display the standings in Streamlit
def display_standings_page(date):
    standings = get_standings(date) 
    # get the conference
    def get_conference(conference):
        return [t for t in standings if t['conferenceName'] == conference]

    # get the division
    def get_division(conference, division):
        return [t for t in conference if t['divisionName'] == division]

    # filter by conference
    eastern = get_conference('Eastern')
    western = get_conference('Western')

    # split by division
    atlantic = get_division(eastern, 'Atlantic')
    metro = get_division(eastern, 'Metropolitan')
    central = get_division(western, 'Central')
    pacific = get_division(western, 'Pacific')

    atlantic_top3 = atlantic[:3]
    metro_top3 = metro[:3]
    east_wild_card = atlantic[3:] + metro[3:]
    east_wild_card.sort(key=lambda t: t['points'], reverse=True)

    # top 3 in each division and wild card - Western Conference
    central_top3 = central[:3]
    pacific_top3 = pacific[:3]
    west_wildcard = central[3:] + pacific[3:]
    west_wildcard.sort(key=lambda t: t['points'], reverse=True)

    # build DataFrames for display
    st.header("Eastern Conference")
    st.subheader("Atlantic")
    display_standings(build_standings_df(atlantic_top3), show_cutoff=False)
    st.subheader("Metropolitan")
    display_standings(build_standings_df(metro_top3), show_cutoff=False)
    st.subheader("Wild Card")
    display_standings(build_standings_df(east_wild_card))

    st.header("Western Conference")
    st.subheader("Central")
    display_standings(build_standings_df(central_top3), show_cutoff=False)
    st.subheader("Pacific")
    display_standings(build_standings_df(pacific_top3), show_cutoff=False)
    st.subheader("Wild Card")
    display_standings(build_standings_df(west_wildcard))