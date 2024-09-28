import streamlit as st
from mplsoccer.pitch import Pitch

def plot_passes(events):
    pitch = Pitch(pitch_color='grass', line_color='white', stripe=True)
    fig, ax = pitch.draw()

    for index, row in events[events["type"] == "Pass"].iterrows():
       pitch.arrows(xstart=row.location[0], ystart=row.location[1], xend=row.pass_end_location[0], yend=row.pass_end_location[1], color='blue', alpha=0.5, ax=ax, width=1)


    st.pyplot(fig)