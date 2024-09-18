import streamlit as st
from dash import dashboard, tne
from home import homefunc
from architechture import sysarcfunc
from requirement import requirementview
from tests import testschedule, testresults

st.set_page_config(page_title="Dashboard", page_icon="🚀", layout="wide")

def main():

    # st.header("🛰️ Rover System Dashboard", divider=True)
    # dashboard()

    # st.header("🧮 Testing and Evaluation", divider=True)
    # tne()

    st.header("🛰️ Instructor Dashboard", divider="violet")

    TABS = ["Home", "Requirements", "Architecture", 
            "Test Schedule", "Test Results", "Grading Wizard"]
    
    tabs = st.tabs(TABS)
    
    with tabs[0]:
        homefunc()
    with tabs[1]:
        requirementview()
    with tabs[2]:
        sysarcfunc()
    with tabs[3]:
        testschedule()
    with tabs[4]:
        testresults()

if __name__ == "__main__":

    main()