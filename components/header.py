import streamlit as st

def header(dataframe, selected_competition_id, selected_season_id, selected_match):
    competition_info = dataframe[dataframe["competition_id"] == selected_competition_id]
    competition_info = competition_info[competition_info["season_id"] == selected_season_id]
    st.markdown("### Campeonato: " + str(competition_info['competition_name'].values[0]) + " - Temporada: " + str(competition_info['season_name'].values[0]))


    match_name = selected_match["home_team"].item() + " x " + selected_match["away_team"].item() + " - " + selected_match["match_date"].item()
    st.markdown(f"##### {match_name}")

    home_team, away_team = st.columns(2)



    

    with home_team:
        st.metric(selected_match["home_team"].item(), selected_match['home_score'].item())
    with away_team:
        st.metric(selected_match["away_team"].item(), selected_match['away_score'].item())


