import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="IPL Dashboard", layout="wide")

st.title("🏏 IPL Data Analysis Dashboard")

# ==============================
# LOAD DATA (FAST - CACHED)
# ==============================
@st.cache_data
def load_data():
    matches = pd.read_csv("../Datasets/matches.csv")
    deliveries = pd.read_csv("../Datasets/deliveries.csv")
    return matches, deliveries

matches, deliveries = load_data()

# ==============================
# SIDEBAR FILTERS
# ==============================
st.sidebar.header("Filters")

teams = sorted(matches["team1"].dropna().unique())
selected_team = st.sidebar.selectbox("Select Team", ["All"] + teams)

players = sorted(deliveries["batsman"].dropna().unique())
selected_player = st.sidebar.selectbox("Search Player", ["All"] + players)

seasons = sorted(matches["Season"].dropna().unique())
selected_season = st.sidebar.selectbox("Select Season", ["All"] + list(seasons))

# ==============================
# APPLY FILTERS
# ==============================
filtered_matches = matches.copy()
filtered_deliveries = deliveries.copy()

if selected_team != "All":
    filtered_matches = filtered_matches[
        (filtered_matches["team1"] == selected_team) |
        (filtered_matches["team2"] == selected_team)
    ]

if selected_season != "All":
    filtered_matches = filtered_matches[
        filtered_matches["Season"] == selected_season
    ]

if selected_player != "All":
    filtered_deliveries = filtered_deliveries[
        filtered_deliveries["batsman"] == selected_player
    ]

# ==============================
# TOP BATSMEN
# ==============================
st.subheader("🔥 Top Batsmen")

top_batsman = filtered_deliveries.groupby("batsman")["batsman_runs"].sum() \
                .sort_values(ascending=False).head(10)

st.bar_chart(top_batsman)

# ==============================
# TOP BOWLERS
# ==============================
st.subheader("🎯 Top Bowlers")

wickets = filtered_deliveries[filtered_deliveries["dismissal_kind"].notna()]

top_bowlers = wickets.groupby("bowler")["player_dismissed"].count() \
                    .sort_values(ascending=False).head(10)

st.bar_chart(top_bowlers)

# ==============================
# TEAM WINS
# ==============================
st.subheader("🏆 Team Wins")

team_wins = filtered_matches["winner"].value_counts()

st.bar_chart(team_wins)

# ==============================
# PLAYER STATS (SEARCH BASED)
# ==============================
if selected_player != "All":
    st.subheader(f"📊 Stats for {selected_player}")

    player_data = deliveries[deliveries["batsman"] == selected_player]

    total_runs = player_data["batsman_runs"].sum()
    balls = len(player_data)
    strike_rate = (total_runs / balls) * 100 if balls > 0 else 0

    st.metric("Total Runs", total_runs)
    st.metric("Balls Played", balls)
    st.metric("Strike Rate", round(strike_rate, 2))

# ==============================
# TOSS IMPACT
# ==============================
st.subheader("🎲 Toss Impact")

toss_win_match_win = matches[matches["toss_winner"] == matches["winner"]]
percentage = len(toss_win_match_win) / len(matches) * 100

st.write(f"Toss win → Match win %: **{percentage:.2f}%**")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | IPL Data Analysis Project")