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


import generate_random_pool as gp
import PortfolioStressTester as ps
import json




st.markdown("# Stress Test")
st.sidebar.markdown("# stress test for portfolio comprising of 3 markets")

# Store the initial value of widgets in session state
st.session_state.visibility = "visible"
st.session_state.disabled = False
df = pd.DataFrame()
uploaded_file = None

col1, col2 = st.columns(2)

with col1:
    pass


with col2:
    pass

st.divider()

