import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)
from io import StringIO

from pathlib import Path
path = Path(myDir)
a=str(path.parent.absolute())
sys.path.append(a)

import PortfolioStressTester as ps
import json




st.markdown("## Portfolio Stress Test")
st.markdown("### Stress test for portfolio comprising of 3 markets")

# Store the initial value of widgets in session state
st.session_state.visibility = "visible"
st.session_state.disabled = False
df = pd.DataFrame()
uploaded_file = None
st.divider()



col1, col2 = st.columns(2)


with col1:
    st.markdown("upload portfolio (this site will not save any user data):")
    st.markdown("上传持仓 **(不会保存任何用户数据)**:")



    uploaded_file = st.file_uploader("Choose a position excel file")
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_excel(uploaded_file)
        st.write(dataframe)


    uploaded_config_file = st.file_uploader("(Optional) Choose a user-specified config file")
    if uploaded_config_file is not None:
        # Convert to a string based IO:
        # Decode the uploaded file to a string
        file_content_str = uploaded_config_file.getvalue().decode("utf-8")
        # Write string to JSON file
        with open("config_user.json", "w") as f:
            json.dump({"message": file_content_str}, f, indent=4)

        st.write(file_content_str)


    with open("config.json", "rb") as file:
        st.download_button(
            label="Download sample config(下载默认测试配置供自定义修改)",
            data=file,
            file_name="sample_config.json",
            mime="json",
        )


    


with col2:
    st.markdown("结果:")
    
    if (st.button("获取结果(100个标的大概需要5分钟,注意按一次即可)", type="primary")):
        if uploaded_file is not None:
            st.write("开始测试。。。")
            if file_content_str is not None:
                st.write("使用用户提供config")
                tester = ps.PortfolioStressTester(config_path="config_user.json",portfolio_path=uploaded_file)
                tester.gen_report()

            else:
                print("使用默认模式config")
                tester = ps.PortfolioStressTester(portfolio_path=uploaded_file)
                tester.gen_report()

            result = pd.read_excel("stress_test_results.xlsx")
            st.write(result)
            st.image("1.png", caption="empirical result")
            st.image("2.png", caption="parametric result")
        else:
            print("Portfolio needed")

st.divider()

