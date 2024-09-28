import streamlit as st
from mplsoccer.pitch import Pitch

def plot_shots(events):
    pitch = Pitch(pitch_color='grass', line_color='white', stripe=True)
    fig, ax = pitch.draw()

    for index, row in events[events["type"] == "Shot"].iterrows():
        pitch.scatter(x=row.location[0], y=row.location[1], ax=ax, color='red')


    st.plotly_chart(fig)