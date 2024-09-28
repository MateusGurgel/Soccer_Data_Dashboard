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

@st.cache_data(ttl=60*60*24)
def get_match_events(match_id: int):
    match_events = sb.events(match_id=match_id)
    return match_events

@st.cache_data(ttl=60*60*24)
def get_event(match_id: int, event: str):
    passes = sb.events(match_id=match_id, split=True, flatten_attrs=False)[event]
    return passes