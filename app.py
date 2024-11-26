# Import streamlit to make frontend components
import streamlit as st

# Import functions from other files, where the View is created
from home import homefunc
from architecture import sysarcfunc
from requirement import requirementview
from tests import testschedule, testresults
from gradingsupport import gradingtaskcompletion

# Set page configuration, page title is the titlebar content, icon also appears on title bar
st.set_page_config(page_title="Dashboard", page_icon="🚀", layout="wide")

# main entrypoint of the application, gets called when the app runs
def main():

    # For the heading on the page
    st.header("🛰️ Instructor Dashboard", divider="violet")

    # create the list of tabs in a list
    TABS = ["Home", "Requirements", "Architecture", 
            "Test Schedule", "Test Results", "Grading Support"]
    # pass the list to make a tab component
    tabs = st.tabs(TABS)
    
    # call each tab and call the function that containes the Page view under the tab section
    with tabs[0]:
        # Home tab view
        homefunc()
    with tabs[1]:
        # Requirements tab view
        requirementview()
    with tabs[2]:
        # Architecture tab view
        sysarcfunc()
    with tabs[3]:
        # Test schedule tab view
        testschedule()
    with tabs[4]:
        # Test results tab view
        testresults()
    with tabs[5]:
        # Grading Wizard tab view
        gradingtaskcompletion()

if __name__ == "__main__":
    main()