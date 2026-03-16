# NHL Scores & Standings

A Streamlit app for viewing live NHL scores and standings, powered by the public NHL API.

## Features

- **Scores** — Live, upcoming, and final scores for any date. Includes goal-by-goal details with period, time, scorer, assists, and strength (PPG/SHG/EN).
- **Standings** — Full NHL standings split by conference, division, and wildcard, with a playoff cutoff line in the wildcard tables.
- **Leaders** - Lists the top 10 players in key stats for both skaters and goalies.
- **Date picker** — View scores and standings for any date via the sidebar.
- **Auto-refresh** — Reload button in the sidebar to update live scores.

## Requirements

- Python 3.9+
- `streamlit`
- `pandas`
- `requests`

Install dependencies:

```bash
pip install streamlit pandas requests
```

## Deployment

Deployed on [Streamlit Community Cloud](https://nhl-scores.streamlit.app/). To deploy your own instance:

1. Fork this repository
2. Connect it to Streamlit Community Cloud
3. Set the main file path to `app.py`

## Running the app

```bash
streamlit run app.py
```

## Data source

All data comes from the public NHL API (`https://api-web.nhle.com/v1/`). No API key is required.
