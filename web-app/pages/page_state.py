import streamlit as st  
from abc import abstractmethod


class PageState:
    def __init__(self):
        pass

    @abstractmethod
    def render(self):
        pass

class LoggedOutState(PageState):
    def __init__(self):
        pass

    def render(self):
        st.title("Please enter the password")
        password = st.text_input("Password")
        st.link_button("Submit", f"http://localhost:8501?password={password}")
