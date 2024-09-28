import streamlit as st
from matplotlib.colors import LinearSegmentedColormap
from mplsoccer import VerticalPitch


def plot_warm_map(match_events):
    pitch = VerticalPitch(line_color="#000009", line_zorder=2)

    fig, ax = pitch.draw(figsize=(4.4, 6.4))

    flamingo_cmap = LinearSegmentedColormap.from_list(
        "Flamingo - 100 colors", ["#e3aca7", "#c03a1d"], N=100
    )

    x, y = match_events["location"].str[0], match_events["location"].str[1]
    pitch.kdeplot(
        x, y, ax=ax, fill=True, levels=100, thresh=0, cut=4, cmap=flamingo_cmap
    )

    st.pyplot(fig)
