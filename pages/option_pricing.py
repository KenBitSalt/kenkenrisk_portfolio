import streamlit as st

def check_integrity(stock_id,Market,Type,Strike_Price,age):
    # check conditions
    st.write('RUN!')

st.markdown("# Option pricing")
st.sidebar.markdown("# option pricing")

# Store the initial value of widgets in session state
st.session_state.visibility = "visible"
st.session_state.disabled = False

col1, col2 = st.columns(2)

with col1:

    if "Market" not in st.session_state:
        st.session_state.Market = "China-A"
    
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

    Strike_Price = st.slider("Set Strike Price", 0, 130, 25)
    #values = st.slider("Select a range of values", 0.0, 100.0, (25.0, 75.0))
    age = st.slider("Set target month of option", 0, 130, 25)
    st.write("Concerning ", age, " month contract")
    st.write("Strike Price (K):", Strike_Price)

with col2:
    if "stock_id" not in st.session_state:
        st.write("STOCK TICKER IS NEEDED")

    text_input = st.text_input(
        "Enter stock ticker 👇",
        label_visibility="visible",
        disabled=st.session_state.disabled,
        key = "stock_id",
        placeholder="Enter ticker for the stock intented",
    )
    
    if "stock_id" in st.session_state:
        st.write(st.session_state.stock_id)

    st.button("Reset", type="primary")

    if st.button("Proceed"):
        if st.session_state.stock_id:
            st.write(st.session_state.stock_id)
        else:
            st.write("still need stock ticker!")
        if st.session_state.Market:
            st.write(st.session_state.Market)
        else:
            st.write("No market!!!")
        st.write(st.session_state.Type)
        st.write(Strike_Price)
        st.write(age)

        check_integrity(st.session_state.stock_id,st.session_state.Market,st.session_state.Type,Strike_Price,age)


st.markdown("## Result:")