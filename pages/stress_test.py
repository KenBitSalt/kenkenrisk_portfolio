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

with open("files/readme.pdf", "rb") as file:
    btn = st.download_button(
    label="下载使用方法和结构介绍文稿",
    data=file,
    file_name="files/readme.pdf",
    mime="text/csv",
)

with open("config.json", "rb") as file:
    st.download_button(
        label="Download sample config(下载默认测试配置供自定义修改)",
        data=file,
        file_name="sample_config.json",
        mime="json",
    )


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
    st.markdown("- **交易日**：`YYYYMMDD` 格式，字符串或 int 均可，程序会自动转换。- **标的代码**：`xxxxx.exchange` 格式（`exchange` 表示交易所，`SZ`/`SH` 为 A 股，`HK` 为港股，`US` 为美股）。- **标的数量**：int。- **行业信息**：（可选，如果没有就要讲config里面的HK_INDEX_CODE改成“恒生指数”）str，用于在 A 股股票缺少特定交易日数据时，用当日行业 return 补齐数据。")


    uploaded_file = st.file_uploader("Choose a position excel file")
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_excel(uploaded_file)
        st.write(dataframe)


    uploaded_config_file = st.file_uploader("(Optional) Choose a user-specified config file")
    file_content_str = None
    if uploaded_config_file is not None:
        # Convert to a string based IO:
        # Decode the uploaded file to a string
        file_content_str = uploaded_config_file.getvalue().decode("utf-8")
        config_data = json.loads(file_content_str)
        # Write string to JSON file
        with open("config_user.json", "w") as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)

        st.write(file_content_str)



    


with col2:
    st.markdown("结果:")
    
    if (st.button("获取结果(100个标的大概需要3分钟,注意按一次即可)", type="primary")):
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

