import streamlit as st

def competition_selector(dataframe):
    competitions = dataframe.drop_duplicates(subset=['competition_name'], inplace=False)
    selected_competition = st.sidebar.selectbox(
        "Escolha um campeonato:",
        competitions["competition_name"],
        placeholder="Selecione um campeonato"
    )
    selected_competition_id = competitions[competitions["competition_name"] == selected_competition]["competition_id"].values[0]

    return selected_competition_id