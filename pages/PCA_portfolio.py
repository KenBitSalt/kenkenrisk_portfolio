import streamlit as st
from io import StringIO
import pandas as pd
import os 
import sys

myDir = os.getcwd()
sys.path.append(myDir)

from pathlib import Path
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)
import generate_random_pool as gp
import run_pca_portfolio as rp

st.markdown("# PCA portfolio")
st.sidebar.markdown("# pca portfolio")

# Store the initial value of widgets in session state
st.session_state.visibility = "visible"
st.session_state.disabled = False
st.session_state.index = "SP500"
use_preset = False
df = pd.DataFrame()
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


with col2:
    

    if use_preset:
        st.markdown("Using Preset Pool")
        df = gp.pool(max=5000).get_df()
        st.dataframe(df)
    else:
        st.write("Using User-Designated Pool")

    

st.divider()