from email.policy import default
import streamlit as st
from statsbombpy import sb

@st.cache_data(ttl=60*60*24)
def get_dataframe():
    dataframe = sb.competitions()
    return dataframe

@st.cache_data(ttl=60*60*24)
def get_match_data(competition_id : int, season_id: int):
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    return matches

dataframe = get_dataframe()

# Selecionar campeonato
competitions = dataframe.drop_duplicates(subset=['competition_name'])
selected_competition = st.sidebar.selectbox(
    "Escolha um campeonato:",
    competitions["competition_name"],
    placeholder="Selecione um campeonato"
)
selected_competition_id = competitions[competitions["competition_name"] == selected_competition]["competition_id"].values[0]
    
# Selecionar temporada
seasons = dataframe[dataframe['competition_name'] == selected_competition].drop_duplicates(subset=['season_name'])
selected_season = st.sidebar.selectbox(
    "Escolha uma temporada:",
    seasons["season_name"],
)
selected_season_id = seasons[seasons["season_name"] == selected_season]["season_id"].values[0]

matches = get_match_data(selected_competition_id, selected_season_id)
selected_match = st.sidebar.selectbox(
    "Escolha um jogo:",
    matches["match_date"]
)

selected_match = matches[matches["match_date"] == selected_match]

st.write(selected_match)

    