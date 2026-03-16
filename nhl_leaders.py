import requests
import pandas as pd
import streamlit as st

"""
Set up a function to get the scoring leaders by category. The function will
take 2 parameters: the category and title for when it's displayed in the
data frame.
This should work for goals, assists, points, penalty minutes, etc.
The function will return a pandas data frame.
"""

@st.cache_data(ttl=300) # cache for 300 seconds (5 minutes)
def get_leaders(category, position, title):
  # empty set to hold the category leaders
  category_leaders = []

  # use the url for the skater or goalie leaders depending on the position parameter
  if position == 'skater':
    url = f"https://api-web.nhle.com/v1/skater-stats-leaders/current?categories={category}&limit=10"
  elif position == 'goalie':
    url = f"https://api-web.nhle.com/v1/goalie-stats-leaders/current?categories={category}&limit=10"

  # error handling
  try:
    response = requests.get(url)
  except requests.exceptions.RequestException:
        print("Error: Could not connect to the NHL API")
        return

  if response.status_code != 200:
        print(f"Error: Unable to fetch data (status code {response.status_code})")
        return

  data = response.json()

  # set a variable holding the leaders that the function will loop through
  leaders = data[category]
  try:
    # loop through the leaders and add to the category_leaders list
    for leader in leaders:
      player = f"{leader['firstName']['default']} {leader['lastName']['default']}"
      team = leader['teamAbbrev']
      if position == 'goalie' and category == 'goalsAgainstAverage':
        value = f"{leader['value']:.2f}" # display GAA with 2 decimal places
      elif position == 'goalie' and category == 'savePctg':
        value = f"{leader['value']:.3f}".lstrip("0") # display SV% with 3 decimal places and remove the leading zero
      else:
        value = leader['value']
      category_leaders.append({'Player': player, 'Team': team, title: value})

    # pandas data frame with tie-aware ranking
    df = pd.DataFrame(category_leaders)
    ranks = []
    rank = 1
    for i, row in enumerate(category_leaders):
      if i > 0 and row[title] == category_leaders[i - 1][title]:
        ranks.append(ranks[-1])
      else:
        rank = i + 1
        ranks.append(rank)
    df.index = [f"T{r}" if ranks.count(r) > 1 else str(r) for r in ranks]
    return df
  except:
    print('Error')   