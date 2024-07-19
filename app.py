import streamlit as st
from dash import dashboard, tne

st.set_page_config(page_title="Dashboard", page_icon="🚀", layout="wide")

def main():

    st.header("🛰️ Rover System Dashboard", divider=True)
    dashboard()

    st.header("🧮 Testing and Evaluation", divider=True)
    tne()

if __name__ == "__main__":

    main()