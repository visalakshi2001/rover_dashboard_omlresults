import streamlit as st
from home import homefunc
from architecture import sysarcfunc
from requirement import requirementview
from tests import testschedule, testresults
from gradingwizard import gradingtaskcompletion

st.set_page_config(page_title="Dashboard", page_icon="🚀", layout="wide")

def main():

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
    with tabs[5]:
        gradingtaskcompletion()

if __name__ == "__main__":

    main()