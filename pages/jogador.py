import streamlit as st
import pandas as pd
from modules.game_data import get_dataframe, get_match_events, get_event
from components.plot_passes import plot_passes
from components.plot_shots import plot_shots
from components.match_selector import match_selector
from components.season_selector import season_selector
from components.competition_selector import competition_selector
from components.header import header
from components.plot_warm_map import plot_warm_map
from components.plot_game_stats import plot_game_stats
from components.player_selector import player_selector


dataframe = get_dataframe()

selected_competition_id = competition_selector(dataframe)
selected_season_id = season_selector(selected_competition_id, dataframe)
selected_match = match_selector(selected_competition_id, selected_season_id)
match_events = get_match_events(selected_match["match_id"].values[0])
selected_player = player_selector(match_events)

player_events = match_events[match_events["player"] == selected_player]

header(dataframe, selected_competition_id, selected_season_id, selected_match)

st.write("### " + selected_player)

passes_col, shots_col, goals_col, goals_conversion, sucess_pass_rate  = st.columns(5)

with passes_col:
    st.metric("Passes", player_events[player_events["type"] == "Pass"].shape[0])
with shots_col:
    st.metric("Chutes", player_events[player_events["type"] == "Shot"].shape[0])
with goals_col:
    st.metric("Gols", player_events[player_events["shot_outcome"] == "Goal"].shape[0])
with goals_conversion:
    st.metric("Conversão de Gols", round(player_events[player_events["shot_outcome"] == "Goal"].shape[0] / player_events[player_events["type"] == "Shot"].shape[0], 2) * 100)
with sucess_pass_rate:
    total_passes = player_events[player_events["type"] == "Pass"].shape[0]
    unsuccessful_passes = player_events[player_events["pass_outcome"] == "Incomplete"].shape[0]
    st.metric("Taxa de Falha de Passes", round((unsuccessful_passes / total_passes) * 100, 2))



kicks_spot_tab, pass_vectors_tab, warm_map_tab = st.tabs(["Chutes ao Gol", "Vetores de Passes", "Mapa de Calor"])

with kicks_spot_tab:
    with st.spinner("Carregando..."):
        st.title("Chutes ao Gol")
        plot_shots(player_events)
        st.text("Veja por onde a pressão na sua defesa está vindo")

with pass_vectors_tab:
    with st.spinner("Carregando..."):
        st.title("Vetores de Passes")
        plot_passes(player_events)
        st.text("Veja como a bola está se movendo no campo")

with warm_map_tab:
    with st.spinner("Carregando..."):
        st.title("Mapa de Calor")
        plot_warm_map(player_events)
        st.text("Veja onde a bola está sendo jogada")

with st.spinner("Carregando..."):
    st.write("### Dados do jogador")
    st.write(player_events)
