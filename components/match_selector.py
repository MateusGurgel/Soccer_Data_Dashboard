from modules.game_data import get_match_data
import streamlit as st

def match_selector(compatiiton_id, season_id):
    matches = get_match_data(compatiiton_id, season_id)
    selected_match = st.sidebar.selectbox(
        "Escolha um jogo:",
        matches["match_date"]
    )
    selected_match = matches[matches["match_date"] == selected_match]

    return selected_match