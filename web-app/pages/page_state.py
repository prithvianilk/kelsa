import streamlit as st  
from abc import abstractmethod


class PageState:
    def __init__(self):
        pass

    @abstractmethod
    def render(self):
        pass