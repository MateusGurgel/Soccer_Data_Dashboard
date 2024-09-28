import streamlit as st
import pandas as pd
from modules.game_data import get_dataframe, get_match_events, get_event
from components.plot_passes import plot_passes
from components.plot_shots import plot_shots
from components.match_selector import match_selector
from components.season_selector import season_selector
from components.competition_selector import competition_selector

dataframe = get_dataframe()

selected_competition_id = competition_selector(dataframe)
selected_season_id = season_selector(selected_competition_id, dataframe)
selected_match = match_selector(selected_competition_id, selected_season_id)
match_events = get_match_events(selected_match["match_id"].values[0])

competition_info = dataframe[dataframe["competition_id"] == selected_competition_id]
competition_info = competition_info[competition_info["season_id"] == selected_season_id]
st.markdown("### Campeonato: " + str(competition_info['competition_name'].values[0]) + " - Temporada: " + str(competition_info['season_name'].values[0]))

match_name = selected_match["home_team"][0] + " x " + selected_match["away_team"][0] + " - " + selected_match["match_date"][0]
st.markdown(f"##### {match_name}")

st.markdown(f"##### Score {selected_match['home_score'][0]} - {selected_match['away_score'][0]}")

pass_tab, kicks_tab, shots_tab = st.tabs(["Pesses x Jogador", "Chutes x Jogador", "Gols x Jogador"])

with pass_tab:
    st.write("### Passes por jogador")
    match_passes = get_event(selected_match["match_id"].values[0], "passes")
    player_passes = pd.DataFrame(match_passes["player"].value_counts())
    st.bar_chart(player_passes)

with kicks_tab:
    st.write("### Chutes por jogador")
    match_shots = get_event(selected_match["match_id"].values[0], "shots")
    player_shots = pd.DataFrame(match_shots["player"].value_counts())
    st.bar_chart(player_shots)

with shots_tab:
    st.write("### Gols por jogador")
    player_goals = pd.DataFrame(match_events[match_events["shot_outcome"] == "Goal"]["player"].value_counts())
    st.bar_chart(player_goals)


kicks_spot_tab, pass_vectors_tab = st.tabs(["Chutes ao Gol", "Vetores de Passes"])

with kicks_spot_tab:
    st.title("Chutes ao Gol")
    plot_shots(match_events)
    st.text("Veja por onde a pressão na sua defesa está vindo")

with pass_vectors_tab:
    st.title("Vetores de Passes")
    plot_passes(match_events)
    st.text("Veja como a bola está se movendo no campo")

st.write(match_events)