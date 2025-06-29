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
    with open("files/Chen_Resume.pdf", "rb") as file:
        btn = st.download_button(
        label="Download a copy of it",
        data=file,
        file_name="files/Chen_Resume.pdf",
        mime="text/csv",
    )
    with open("files/陈思懿简历.pdf", "rb") as file:
        btn = st.download_button(
        label="或 者 一 份 中 文 简 历",
        data=file,
        file_name="files/陈思懿简历.pdf",
        mime="text/csv",
    )
        
    
    st.markdown("My work and studies focus on secondary market derivatives and asset management.")
    st.markdown("contact me via:")
    st.markdown("- sc4793@columbia.edu")
    st.markdown("- (551)220-8597")


    st.markdown("Also visit my wechat public account ***四十四二十二*** for equity derivatives analysis content written in Chinese.")
    #st.markdown("")

with col2:
    st.image("files/me.jpg", caption="[Some digital portrait of arthur 2024]")




st.divider()