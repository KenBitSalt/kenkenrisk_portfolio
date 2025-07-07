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
    constract_dur_years = int(st.slider("Set contract duration (years): ", 1, 10, 1))
    simulation_times = int(st.slider("Set simulation times: ", 20, 300, 1))
    steps = int(st.slider("Set simulation steps: ", 12, 365, 1))
    engine = MonteCarloEngine(S0=100, r=0.03, sigma=0.2, T=1, N=steps, M=simulation_times)
    paths = engine.simulate_paths()
    #sims = np.arange(1,len(paths)+1)
    arr = [str(i) for i in range(1, len(paths)+1)]
    print(len(arr))
    print(len(paths))
    show_sim_df = pd.DataFrame(paths)
    st.line_chart(show_sim_df.T)

with col2:
    contract_type = st.radio(
    "Select contract genre: ",
    ["***Accumulator***", "***FCN***", "***CCN***","***Phoenix***"],
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