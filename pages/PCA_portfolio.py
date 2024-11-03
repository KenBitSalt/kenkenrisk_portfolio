import streamlit as st

st.markdown("# PCA portfolio")
st.sidebar.markdown("# pca portfolio")

# Store the initial value of widgets in session state
st.session_state.visibility = "visible"
st.session_state.disabled = False

col1, col2 = st.columns(2)

with col1:
    st.text_input(
        "Placeholder for the other text input widget",
        "This is a placeholder",
        key="placeholder",
    )
    values = st.slider("Select a range of values", 0.0, 100.0, (25.0, 75.0))
    age = st.slider("Set target month of option", 0, 130, 25)
    st.write("I'm ", age, "years old")
    st.write("Values:", values)

with col2:
    text_input = st.text_input(
        "Enter stock ticker 👇",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        placeholder=st.session_state.placeholder,
    )