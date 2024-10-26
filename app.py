import streamlit as st

st.title('Persona: Personalised Portfolio Builder') 

class Pages_switch():
    st.sidebar.page_link("app.py", label="Home")
    st.sidebar.page_link("pages/Questions.py", label="Questionnaire")
    st.sidebar.page_link("pages/DashBoard.py", label="Dashboard")

Pages_switch()