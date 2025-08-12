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




st.markdown("## Portfolio Stress Test")
st.markdown("### Stress test for portfolio comprising of 3 markets")

# Store the initial value of widgets in session state
st.session_state.visibility = "visible"
st.session_state.disabled = False
df = pd.DataFrame()
uploaded_file = None

col1, col2 = st.columns(2)
st.divider()

with col1:
    st.markdown("upload portfolio (this site will not save any user data):")
    st.markdown("上传持仓 (本站不会保存任何用户数据):")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_excel(uploaded_file)
        st.write(dataframe)


with col2:
    st.markdown("结果:")
    
    if (st.button("获取结果", type="primary")):
        if uploaded_file is not None:
            print("开始测试。。。")
        else:
            print("Portfolio needed")

st.divider()

