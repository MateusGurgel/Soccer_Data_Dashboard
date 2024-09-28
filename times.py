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

dataframe = get_dataframe()

selected_competition_id = competition_selector(dataframe)
selected_season_id = season_selector(selected_competition_id, dataframe)
selected_match = match_selector(selected_competition_id, selected_season_id)
match_events = get_match_events(selected_match["match_id"].values[0])

header(dataframe, selected_competition_id, selected_season_id, selected_match)

pass_tab, kicks_tab, shots_tab, game_stats = st.tabs(["Pesses x Jogador", "Chutes x Jogador", "Gols x Jogador", "Game Stats"])

with pass_tab:
    with st.spinner("Carregando..."):
        st.write("### Passes por jogador")
        match_passes = get_event(selected_match["match_id"].values[0], "passes")
        player_passes = pd.DataFrame(match_passes["player"].value_counts())
        st.bar_chart(player_passes)

with kicks_tab:
    with st.spinner("Carregando..."):
        st.write("### Chutes por jogador")
        match_shots = get_event(selected_match["match_id"].values[0], "shots")
        player_shots = pd.DataFrame(match_shots["player"].value_counts())
        st.bar_chart(player_shots)

with shots_tab:
    with st.spinner("Carregando..."):
        st.write("### Gols por jogador")
        player_goals = pd.DataFrame(match_events[match_events["shot_outcome"] == "Goal"]["player"].value_counts())
        st.bar_chart(player_goals)

with game_stats:
    st.markdown("### Estatísticas do Jogo")
    plot_game_stats(match_events, selected_match)



kicks_spot_tab, pass_vectors_tab, warm_map_tab = st.tabs(["Chutes ao Gol", "Vetores de Passes", "Mapa de Calor"])

with kicks_spot_tab:
    with st.spinner("Carregando..."):
        st.title("Chutes ao Gol")
        plot_shots(match_events)
        st.text("Veja por onde a pressão na sua defesa está vindo")

with pass_vectors_tab:
    with st.spinner("Carregando..."):
        st.title("Vetores de Passes")
        plot_passes(match_events)
        st.text("Veja como a bola está se movendo no campo")

with warm_map_tab:
    with st.spinner("Carregando..."):
        st.title("Mapa de Calor")
        plot_warm_map(match_events)
        st.text("Veja onde a bola está sendo jogada")

with st.spinner("Carregando..."):
    st.write("### Dados da Partida")
    st.write(match_events)