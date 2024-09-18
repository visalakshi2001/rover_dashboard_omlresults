import streamlit as st
import pandas as pd


def homefunc():
    sections = st.columns([0.4, 0.6])

    with sections[0]:
        top = st.container(border=True, height=400)
        bottom = st.container(border=True, height=400)

        top.markdown("<h5>Project Overview</h5>", True)
        bottom.markdown("<h5>Project Summary</h5>", True)

    with sections[1]:
        cont = st.container(border=True, height=800)

        cont.markdown("<h5>Group Summary</h5>", True)