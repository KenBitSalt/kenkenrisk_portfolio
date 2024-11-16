import streamlit as st
from io import StringIO
import pandas as pd
import os 
import sys
import altair as alt
from vega_datasets import data

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
df = pd.DataFrame()
uploaded_file = None
col1, col2 = st.columns(2)

with col1:
    st.radio(
        "Select index as benchmark",
        key="index",
        options=["SPY", "CSI500"],
    )

    st.radio(
        "Maximize or minimize optimization objective",
        key="direction",
        options=["Maximize", "Minimize"],
    )

    range = int(st.slider("Set backtest range", 182, 730, 365))


    use_preset = st.radio(
        "Portfolio Stock Pool from:",
        [":rainbow[use_preset]", "***User-Provided***"],
        captions=[
            "A randomly generated pool",
            "upload csv file.",
        ],
    )

    #st.markdown("OR upload csv file containing stock pool and optimized objective for each item By UNCHECKING the previous box")
    if use_preset != ":rainbow[use_preset]":
        uploaded_file = st.file_uploader("Must Cols: [stock_id]: ticker, [objective]: optimzation objective")



with col2:

    if use_preset == ":rainbow[use_preset]":
        df = gp.pool(range=range, max=5000).get_df()
        st.markdown("Using Preset Pool of len: %s" % len(df))
    else:
        st.write("Using User-Designated Pool")

    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        # To convert to a string based IO:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.markdown("User Uploaded Pool of len: %s" % len(dataframe))

    if st.session_state.index in ["SPY","CSI500"]:
        import check_stock as cs
        if st.session_state.index == "SPY":
            index_hist = cs.get_daily("SPY",length = range)
            print(index_hist)

    if (len(index_hist)>=1):
        st.line_chart(index_hist, x="Date", y="Close")

    if (use_preset == ":rainbow[use_preset]") & (len(df)>=1):
        hist = alt.Chart(df).mark_bar().encode(x = alt.X('objective', 
                                                        bin = alt.BinParams(maxbins = 30)), 
                                                y = 'count()') 
        # showing the histogram 
        st.altair_chart(hist, key="alt_chart")

        


st.divider()

