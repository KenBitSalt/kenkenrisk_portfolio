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
path_simulated = False

col1, col2 = st.columns(2)

with col1:
    constract_dur_years = int(st.slider("Set contract duration (years): ", 1, 10, 1))
    simulation_times = int(st.slider("Set simulation times: ", 50, 3000, 1500))

    steps = constract_dur_years*12
    st.markdown("simulated steps is **(%s)**" % steps)

    #steps = int(st.slider("Set simulation steps: ", 12, 365, 1))
    S0, r, Vol = None, None, None

    S0 = st.number_input(
    "Initial Stock Price", value=100, placeholder="Type-in stock price..."
)
    
    r = st.number_input(
    "risk-free rate", value=0.05, placeholder="Type-in risk-free rate..."
)
    
    sigma = st.number_input(
    "sigma", value=0.06, placeholder="Type-in sigma rate..."
)
    st.write("The current S0, r, vol: ", S0, r, sigma)


with col2:
    contract_type = st.radio(
    "Select contract genre: ",
    ["***Accumulator***", "***FCN***", "***DCN***","***Phoenix***"],
    captions=[
        "雪球",
        "每期观察是否敲出；未敲出时固定支付票息。若未敲出但敲入了，到期本金跟随标的表现。",
        "每期观察一次价格是否在敲入区间内，如果是，就支付固定票息；若到期时发生敲入，则本金有损失。",
        "每期只要没有敲入，就支付票息；敲入后停止支付票息，若到期低于敲入价，则本金损失。(没有敲出)"
    ],
)
    

    #if S0 and r and Vol:
    try:
        engine = MonteCarloEngine(S0=S0, r=r, sigma=sigma, T=1, N=steps, M=simulation_times)
        paths = engine.simulate_paths()
        path_simulated = True
        #sims = np.arange(1,len(paths)+1)
        arr = [str(i) for i in range(1, len(paths)+1)]
        print(len(arr))
        print(len(paths))
        show_sim_df = pd.DataFrame(paths)
        st.line_chart(show_sim_df.T)

    except:
        st.markdown("Parameters on left not done yet")
    
    

st.divider()



col3, col4 = st.columns(2)

with col3:
    if path_simulated:
        st.write("The current contract type: ", contract_type)

        if contract_type == "***Accumulator***":
            payoff = pf.classic_snowball_payoff
        elif contract_type == "***FCN***":
            payoff = pf.FCN_payoff
        elif contract_type == "***DCN***":
            payoff = pf.DCN_payoff
        elif contract_type == "***Phoenix***":
            payoff = pf.phoenix_payoff
        
            
        engine.set_payoff(lambda paths: payoff(paths, K_in=80, K_out=105, coupon=0.12, S0=100))
        price = engine.price()
        st.markdown("Price: ***%s***" % price)
    else:
        st.markdown("please simulated path first!")



with col4:

    st.markdown("Greeks simulations: ")

    greeks = engine.estimate_greeks_grid()
    #print(greeks['delta_array'])
    greeks_df = pd.DataFrame(greeks)
    #print(greeks_df)


    st.line_chart(greeks_df, x="S0_array", y="delta_array")
    st.line_chart(greeks_df, x="S0_array", y="gamma_array")
    st.line_chart(greeks_df, x="S0_array", y="vega_array")
    st.line_chart(greeks_df, x="S0_array", y="vanna_array")