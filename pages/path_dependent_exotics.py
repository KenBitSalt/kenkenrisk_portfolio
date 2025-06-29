import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

from pathlib import Path
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)

from sim_engine.monte import MonteCarloEngine
import sim_engine.payoffs as pf

ready = False
show = False
visible_strike = False


col1, col2 = st.columns(2)

with col1:
    simulation_times = int(st.slider("Set simulation times: ", 50, 1000, 1))
    steps = int(st.slider("Set simulation steps: ", 12, 365, 1))
    engine = MonteCarloEngine(S0=100, r=0.03, sigma=0.2, T=1, N=steps, M=simulation_times)
    paths = engine.simulate_paths()

    show_sim_df = pd.DataFrame(paths,columns= steps)
    st.line_chart(show_sim_df)

with col2:
    contract_type = st.radio(
    "Select contract genre: ",
    [":accumulator[Comedy]", "***FCN***", "***CCN***"],
    captions=[
        "雪球",
        "not done yet",
        "not done yet",
    ],
)

st.divider()


if contract_type == ":accumulator[Comedy]":
    col3, col4 = st.columns(2)

    with col3:
        print('col3')

    with col4:
        if show:
            print('col4')