import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st

def team_logo(abbrev):
  url = f"https://assets.nhle.com/logos/nhl/svg/{abbrev}_light.svg"
  return f'<img src="{url}" height="28px" style="vertical-align:middle; margin:0 4px;">'

def get_period_label(period):
  """Convert period number to display label."""
  labels = {1: '1st', 2: '2nd', 3: '3rd', 4: 'OT', 5: 'SO'}
  return labels.get(period, str(period))

def display_goals(goals):
  """Display goal scorers with assists and strength indicators."""
  if not goals:
    return
  lines = []
  for goal in goals:
    period_label = get_period_label(goal['period'])
    time_in = goal['timeInPeriod']
    goal_scorer = goal['name']['default']
    team = goal['teamAbbrev']

    # get team strength on the goal (even, PP, SH)
    strength = goal['strength']
    if strength == "pp":
      strength_str = " (PPG)"
    elif strength == "sh":
      strength_str = " (SHG)"
    else:
      strength_str = ""

    # account for if a goal is scored into an empty net
    modifier = goal['goalModifier']
    if modifier == "empty-net":
      modifier_str = " (EN)"
    else:
      modifier_str = ""

    # build the assist string
    assist_scorers = [a['name']['default'] for a in goal['assists']]

    if period_label == 'SO':
      lines.append(f"&nbsp;&nbsp;&nbsp;&nbsp;{period_label}&nbsp; **{team}** {goal_scorer}{strength_str}")
    elif assist_scorers:
      lines.append(f"&nbsp;&nbsp;&nbsp;&nbsp;{period_label}&nbsp; **{team}** {time_in} {goal_scorer}, Assists: {', '.join(assist_scorers)}{strength_str}"
            f"{modifier_str}")
    else:
      lines.append(f"&nbsp;&nbsp;&nbsp;&nbsp;{period_label}&nbsp; **{team}** {time_in} {goal_scorer} (Unassisted){strength_str}{modifier_str}")
  
  st.markdown("<br>".join(lines), unsafe_allow_html=True)

def get_scores(date):
  url = f"https://api-web.nhle.com/v1/score/{date}"
  MY_TIMEZONE = ZoneInfo('US/Eastern')

  # error handling
  try:
    response = requests.get(url)
  except requests.exceptions.RequestException:
    st.error("Error: Could not connect to the NHL API")
    return

  if response.status_code != 200:
    print(f"Error: Unable to fetch scores (status code {response.status_code})")
    return

  data = response.json()
  games = data['games']

  # check if no games scheduled
  if not games:
    print("No games scheduled for this date.")
    return

  # loop through the games
  for game in games:
    away_team = game['awayTeam']['abbrev']
    home_team = game['homeTeam']['abbrev']
    game_state = game['gameState']

    # if the game is ongoing, get the score
    if game_state in ("LIVE", "CRIT"):
      away_score = game['awayTeam']['score']
      home_score = game['homeTeam']['score']
      period = game['period']
      period_label = get_period_label(period)
      time_left = game['clock']['timeRemaining']
      in_intermission = game['clock']['inIntermission']

      if in_intermission:
        st.markdown(f"### {team_logo(away_team)} {away_team} {away_score} - {home_score} {home_team} {team_logo(home_team)} {period_label} INT", unsafe_allow_html=True)
      else:
        st.markdown(f"### {team_logo(away_team)} {away_team} {away_score} - {home_score} {home_team} {team_logo(home_team)}{period_label} {time_left}", unsafe_allow_html=True)

      display_goals(game.get('goals', []))

    # if the game has yet to start, show the game and the start time
    elif game_state in ("PRE", "FUT"):
      utc_time = datetime.fromisoformat(game['startTimeUTC'].replace('Z', '+00:00'))
      eastern_time = utc_time.astimezone(MY_TIMEZONE)
      st.markdown(f"### {team_logo(away_team)} {away_team} @ {home_team} {team_logo(home_team)} {eastern_time.strftime('%-I:%M %p')}", unsafe_allow_html=True)

    # if the game is over, show the final score
    elif game_state in ("OFF", "FINAL"):
      away_score = game['awayTeam']['score']
      home_score = game['homeTeam']['score']
      if game['gameOutcome']['lastPeriodType'] == "REG":
        end_result = "Final"
      elif game['gameOutcome']['lastPeriodType'] == "OT":
        end_result = "Final/OT"
      elif game['gameOutcome']['lastPeriodType'] == "SO":
        end_result = "Final/SO"

      st.markdown(f"### {team_logo(away_team)} {away_team} {away_score} - {home_score} {home_team} {team_logo(home_team)} {end_result}", unsafe_allow_html=True)

      display_goals(game.get('goals', []))