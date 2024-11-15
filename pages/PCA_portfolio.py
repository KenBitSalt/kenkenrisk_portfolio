import streamlit as st
from io import StringIO
import pandas as pd

st.markdown("# PCA portfolio")
st.sidebar.markdown("# pca portfolio")

# Store the initial value of widgets in session state
st.session_state.visibility = "visible"
st.session_state.disabled = False
st.session_state.index = "SP500"
use_preset = False

col1, col2 = st.columns(2)

with col1:
    st.radio(
        "Select index as benchmark",
        key="index",
        options=["CSI-500", "SP500"],
    )

    st.radio(
        "Maximize or minimize optimization objective",
        key="direction",
        options=["Maximize", "Minimize"],
    )

with col2:
    st.markdown("Upload a csv file containing selectable pool and optimized objective for each item")
    uploaded_file = st.file_uploader("Must Cols: [stock_id]: ticker, [objective]: optimzation objective")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        # To convert to a string based IO:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.dataframe(
            dataframe,
            hide_index=False,
        )

    use_preset = st.checkbox("Use preset pool")

    if use_preset:
        st.write("Using Preset pool")
    else:
        st.write("Using User-Designated Pool")

st.divider()