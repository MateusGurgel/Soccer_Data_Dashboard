import streamlit as st
from modules.game_data import get_dataframe, get_match_events
from components.match_selector import match_selector
from components.season_selector import season_selector
from components.competition_selector import competition_selector
from components.header import header

with st.spinner("Carregando..."):
    dataframe = get_dataframe()


selected_competition_id = competition_selector(dataframe)
selected_season_id = season_selector(selected_competition_id, dataframe)
selected_match = match_selector(selected_competition_id, selected_season_id)
match_events = get_match_events(selected_match["match_id"].values[0])

header(dataframe, selected_competition_id, selected_season_id, selected_match)


show_only_goals = st.checkbox("Mostrar apenas dados de gols", value=False)

if show_only_goals:
    match_events = match_events[match_events["type"] == "Shot"]
    match_events = match_events[match_events["shot_outcome"] == "Goal"]

show_only_player_specific = st.checkbox("Mostrar apenas dados de um jogador específico", value=False)

if show_only_player_specific:
    player_name = st.text_input("Nome do jogador")
    match_events = match_events[match_events["player"] == player_name]

st.write(match_events)

#download csv
st.download_button("Download CSV", dataframe.to_csv(), "data.csv", "text/csv")