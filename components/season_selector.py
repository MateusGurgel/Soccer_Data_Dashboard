import streamlit as st


def season_selector(competition_id, dataframe):

    seasons = dataframe[dataframe["competition_id"] == competition_id].drop_duplicates(
        subset=["season_name"]
    )

    selected_season = st.sidebar.selectbox(
        "Escolha uma temporada:",
        seasons["season_name"],
    )

    selected_season_id = seasons[seasons["season_name"] == selected_season][
        "season_id"
    ].values[0]

    return selected_season_id
