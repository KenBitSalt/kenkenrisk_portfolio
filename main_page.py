import streamlit as st
from datetime import datetime

st.markdown("# Kenken Risk Portfolio")
st.sidebar.markdown("# About this site:")
st.sidebar.markdown("I'm Ken, a former risk/portfolio manager and current MSOR (conc. financial markets) student at Columbia Engineering.")
st.sidebar.markdown("I focus on financial engineering and risk management and derivatives.")
# Store the initial value of widgets in session state
st.session_state.visibility = "visible"
st.session_state.disabled = False

col1, col2 = st.columns(2)

with col1:
    st.markdown("This site is a toy deployment of some highlights of my previous work, detailed in a resume provided below.")
    with open("files/Chen Resume.pdf", "rb") as file:
        btn = st.download_button(
        label="Download a copy of my resume",
        data=file,
        file_name="files/Chen Resume.pdf",
        mime="text/csv",
    )
    st.markdown("My work and studies focus on secondary market derivatives and asset management.")
    st.markdown("contact me via:")
    st.markdown("- sc4793@columbia.edu")
    st.markdown("- (551)220-8597")


with col2:
    st.image("files/me.jpg", caption="[A digital portrait of me 2024]")




