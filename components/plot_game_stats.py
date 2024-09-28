import streamlit as st

def plot_game_stats(match_events, selected_match):
    home_team_stats, away_team_stats, game_stats = st.tabs(["Estatísticas do time da casa", "Estatísticas do time visitante", "Estatísticas do jogo"])

    with home_team_stats:
        shots, passes = st.columns(2)
        with shots:
            st.metric("Chutes ao gol", match_events["type"][match_events["type"] == "Shot"][match_events["team"] == selected_match["home_team"].item()].count())

        with passes:
            st.metric("Passes", match_events["type"][match_events["type"] == "Pass"][match_events["team"] == selected_match["home_team"].item()].count())

    with away_team_stats:
        shots, passes = st.columns(2)
        with shots:
            st.metric("Chutes ao gol", match_events["type"][match_events["type"] == "Shot"][match_events["team"] == selected_match["away_team"].item()].count())

        with passes:
            st.metric("Passes", match_events["type"][match_events["type"] == "Pass"][match_events["team"] == selected_match["away_team"].item()].count())

    with game_stats:
        shots, passes = st.columns(2)
        with shots:
            st.metric("Chutes ao gol", match_events["type"][match_events["type"] == "Shot"].count())

        with passes:
            st.metric("Passes", match_events["type"][match_events["type"] == "Pass"].count())