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

import check_stock as cs
import run_option_pricing as rp

show = False
visible_strike = False

def check_integrity(stock_id,Market,Type,Model,Strike_Price,age):
    # check conditions
    if (isinstance(stock_id, str)) & (len(stock_id) > 0):
        if isinstance(Market, str):
            if isinstance(Type, str):
                if isinstance(Model, str):
                    if isinstance(Strike_Price, float):
                        if isinstance(age, int):
                            return True
                        else:
                            st.write('age issue')
                            return False
                    else:
                        st.write('Strike price issue')
                        return False
                else: 
                    st.write('Model issue')
                    return False
            else:
                st.write('Type issue')
                return False
        else:
            st.write('Market issue')
            return False
    else:
        return False

st.markdown("# Option pricing")
st.sidebar.markdown("# option pricing")

# Store the initial value of widgets in session state
st.session_state.visibility = "visible"
st.session_state.disabled = False

col1, col2 = st.columns(2)

with col1:

    if "Market" not in st.session_state:
        st.session_state.Market = "U.S."
    
    if "Type" not in st.session_state:
        st.session_state.Type = "Call"

    #st.checkbox("Stock Market", key="disabled")
    st.radio(
        "Select Stock Market for this calculation",
        key="Market",
        options=["U.S.", "China-A"],
    )

    st.radio(
        "Select Contract type for this calculation",
        key="Type",
        options=["Call", "Put"],
    )

    #Strike_Price = float(st.slider("Set Strike Price", 0.0, 1000.0, 25.0))
    #values = st.slider("Select a range of values", 0.0, 100.0, (25.0, 75.0))
    age = int(st.slider("Set target month of option", 0, 36, 12))
    risk_free = float(st.slider("Set risk-free rate", 0.0, 1.0, 0.1))


with col2:
    if "stock_id" not in st.session_state:
        st.write("STOCK TICKER IS NEEDED")

    text_input = st.text_input(
        "👇 Enter stock ticker 👇",
        label_visibility="visible",
        disabled=st.session_state.disabled,
        key = "stock_id",
        placeholder="Enter ticker for the stock intented (e.g. msft)",
    )
    
    if "stock_id" in st.session_state:
        if (len(st.session_state.stock_id) >= 1) :
            stock_hist = cs.get_daily(st.session_state.stock_id)
            current_price = stock_hist.loc[len(stock_hist)-1,"Close"]
            stock_hist['Strike'] = current_price
            volatility = rp.calculate_historical_volatility(stock_hist)
            #st.line_chart(stock_hist, x="Date", y="Close")
            st.write("%s has latest price: %s" % (st.session_state.stock_id, current_price))
            visible_strike = True
        
    if visible_strike:
        Strike_Price = float(st.slider("👇 Then Set Strike Price 👇", current_price*0.2, current_price*2, current_price))
        stock_hist['Strike'] = Strike_Price

    if "Model" not in st.session_state:
        st.session_state.Model = "Black-Scholes"

    #st.checkbox("Stock Market", key="disabled")
    st.radio(
        "Implemented Model for this calculation",
        key="Model",
        options=["Black-Scholes", "others (not yet deployed)"],
    )

    #st.button("Reset", type="primary")

    #if st.button("Proceed"):
        #if st.session_state.stock_id:
        #    st.write("Target: ", st.session_state.stock_id)
        #else:
        #    st.write("still need stock ticker!")
        #if st.session_state.Market:
        #    st.write("Market:",st.session_state.Market)
        #else:
        #    st.write("No market!!!")
        #st.write("Contract: ", st.session_state.Type)
        #st.write("Strike: ",Strike_Price)
        #st.write("Time to Maturity: ",age)
        #st.write("Risk-free rate: ",risk_free)
    if ("stock_id" in st.session_state) & (len(st.session_state.stock_id) >= 1) & (Strike_Price >= 0) :
        if check_integrity(st.session_state.stock_id,st.session_state.Market,st.session_state.Type,st.session_state.Model,Strike_Price,age):
            st.write("PLEASE REFER TO THE RESULT")
            show = True

        else:
            st.write("Data is not integral, try again")


st.markdown("## Result:")
if (len(st.session_state.stock_id) >= 1) :
    #stock_hist = cs.get_daily(st.session_state.stock_id)
    st.line_chart(stock_hist, x="Date", y=["Close","Strike"])
    #st.markdown('stock "%s" in [%s] ...' % (st.session_state.stock_id, st.session_state.Market))
    if show:
        #print(len(stock_hist)-1)
        #st.markdown('Current Price [%s], Volatility [%s] ...' % (str(current_price), str(volatility)))
        model = rp.BlackScholesModel(current_price, Strike_Price,age/12,risk_free,volatility)
        deltas = rp.BlackScholesGreeks(current_price, Strike_Price,age/12,risk_free,volatility)
        if st.session_state.Type == 'Call':
            price = model.call_option_price()
            st.markdown('📚 Call Price is: %s 📚 Volatility is: %s' % (price, volatility) )
            delta = deltas.delta_call()
            gamma = deltas.gamma()
            theta = deltas.theta_call()
            vega = deltas.vega()
            rho = deltas.rho_call()
            st.markdown('### With Greeks: ')
            st.markdown('- delta: %s' % delta)
            st.markdown('- gamma: %s' % gamma)
            st.markdown('- theta: %s' % theta)
            st.markdown('- vega: %s' % vega)
            st.markdown('- rho: %s' % rho)
        else:
            price = model.put_option_price()
            st.markdown('### Put Price is: %s' % price)
            delta = deltas.delta_put()
            gamma = deltas.gamma()
            theta = deltas.theta_put()
            vega = deltas.vega()
            rho = deltas.rho_put()
            st.markdown('### With Greeks: ')
            st.markdown('- delta: %s' % delta)
            st.markdown('- gamma: %s' % gamma)
            st.markdown('- theta: %s' % theta)
            st.markdown('- vega: %s' % vega)
            st.markdown('- rho: %s' % rho)
        
            

else:
    st.markdown('Enter the required information first')