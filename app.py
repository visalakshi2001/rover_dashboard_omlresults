import streamlit as st
from dash import dashboard

st.set_page_config(page_title="Dashboard", page_icon="🚀", layout="wide")

def main():

    st.header("🛰️ Rover System Dashboard", divider=True)
    dashboard()

if __name__ == "__main__":

    main()