import streamlit as st
from statsbombpy import sb
import pandas as pd
from mplsoccer.pitch import Pitch
import seaborn as sns


@st.cache_data(ttl=60*60*24)
def get_dataframe():
    dataframe = sb.competitions()
    return dataframe

@st.cache_data(ttl=60*60*24)
def get_match_data(competition_id : int, season_id: int):
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    return matches

@st.cache_data(ttl=60*60*24)
def get_match_events(match_id: int):
    match_events = sb.events(match_id=match_id)
    return match_events

@st.cache_data(ttl=60*60*24)
def get_event(match_id: int, event: str):
    passes = sb.events(match_id=match_id, split=True, flatten_attrs=False)[event]
    return passes

def plot_shots(events):
    pitch = Pitch(pitch_color='grass', line_color='white', stripe=True)
    fig, ax = pitch.draw()

    for index, row in events[events["type"] == "Shot"].iterrows():
        pitch.scatter(x=row.location[0], y=row.location[1], ax=ax, color='red')


    st.plotly_chart(fig)

def plot_passes(events):
    pitch = Pitch(pitch_color='grass', line_color='white', stripe=True)
    fig, ax = pitch.draw()

    for index, row in events[events["type"] == "Pass"].iterrows():
       pitch.arrows(xstart=row.location[0], ystart=row.location[1], xend=row.pass_end_location[0], yend=row.pass_end_location[1], color='blue', alpha=0.5, ax=ax, width=1)


    st.pyplot(fig)

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
match_events = get_match_events(selected_match["match_id"].values[0])

match_passes = get_event(selected_match["match_id"].values[0], "passes")
match_shots = get_event(selected_match["match_id"].values[0], "shots")

player_passes = pd.DataFrame(match_passes["player"].value_counts())
player_shots = pd.DataFrame(match_shots["player"].value_counts())
player_goals = pd.DataFrame(match_events[match_events["shot_outcome"] == "Goal"]["player"].value_counts())

match_name = selected_match["home_team"][0] + " x " + selected_match["away_team"][0] + " - " + selected_match["match_date"][0]

st.markdown("### Campeonato: " + selected_competition + " - Temporada: " + selected_season)
st.markdown(f"##### {match_name}")
st.markdown(f"##### Score {selected_match['home_score'][0]} - {selected_match['away_score'][0]}")

pass_tab, kicks_tab, shots_tab = st.tabs(["Pesses x Jogador", "Chutes x Jogador", "Gols x Jogador"])

with pass_tab:
    st.write("### Passes por jogador")
    st.bar_chart(player_passes)

with kicks_tab:
    st.write("### Chutes por jogador")
    st.bar_chart(player_shots)

with shots_tab:
    st.write("### Gols por jogador")
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

kicks_per_time_tab = st.tabs(["Chutes ao Gol por tempo de partidad"])

st.write(match_events)