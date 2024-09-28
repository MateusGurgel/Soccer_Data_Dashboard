import streamlit as st

def player_selector(match_events):
    players = match_events["player"].dropna().unique()

    selected_match = st.sidebar.selectbox(
        "Escolha um jogo:",
        players
    )

    return selected_match

