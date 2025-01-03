import streamlit as st
from io import StringIO
import pandas as pd
import os 
import sys
import altair as alt
from vega_datasets import data
import check_stock as cs

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


with col2:
    range_date = int(st.slider("Set backtest range", 182, 730, 365))


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



st.divider()

if st.button("Click: Produce PCA portfolio", use_container_width=True):

    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        # To convert to a string based IO:
        # Can be used wherever a "file-like" object is accepted:
        df = pd.read_csv(uploaded_file)

    # reproduce pool
    else:
        df = gp.pool(range=range_date, max=6000).get_df()

    st.markdown("Using Pool of len: %s" % len(df))

    col1, col2 = st.columns(2)
    with col1:
        hist = alt.Chart(df).mark_bar().encode(x = alt.X('objective', 
                                                        bin = alt.BinParams(maxbins = 30)), 
                                                y = 'count()') 
        # showing the histogram 
        st.altair_chart(hist, key="alt_chart")


    # get index performance
    index_hist = cs.get_daily(st.session_state.index,length = range_date)
    print(index_hist)
    with col2:
        if (len(index_hist)>=1):
            st.line_chart(index_hist, x="Date", y="Close")

    # get stock performance from each of the df

    progress_text = "Query stock dayline. Please wait."
    my_bar = st.progress(0, text=progress_text)


    for i in range(len(df)):
        stock = df['stock_id'].to_list()[i]
        stock_df = cs.get_daily(stock,length=range_date)
        my_bar.progress((i + 1)/len(df), text="Query %s dayline. Please wait." % stock)

    my_bar.empty()


