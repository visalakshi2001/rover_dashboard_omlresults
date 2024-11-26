# To make components
import streamlit as st
# to read data
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

# import the view for issues from issues.py
from issues import issuesinfo, warningdetails

# ########## Grading Wizard VIEW FUNCTION
def gradingtaskcompletion():
    # read the CSV data file for all assigned tasks
    roles = pd.read_csv("reports/Tasks_Rover.csv", index_col=0)

    # make two columns of width 60% and 40%
    sections = st.columns([0.6, 0.4])

    # call first column and continue the design under
    with sections[0]:
        
        taskscompleted = roles[["StudentName", "Responsibilities", "Description"]].rename({"Responsibilities": "Role"}, axis=1).copy()
        taskscompleted["Completed"] = pd.notnull(roles["Outputs"])
        
        totalTasks = len(taskscompleted["Completed"])

        metriccols = st.columns(3)

        metriccols[0].metric(label="✅ Task Completed", value=f'{taskscompleted["Completed"].sum()/totalTasks*100:.1f}%', 
        delta=f'Total Tasks: {totalTasks}')

        issues_dict = warningdetails()

        issueCount = sum([len(issues_dict[issuetype]) for issuetype in issues_dict])
        # st.write()

        metriccols[1].metric(label='⚠️ Issues Raised', value=issueCount, delta=f'Urgent issues: {len(issues_dict["testreq"])}')

        metriccols[2].metric(label='🌟 Successful Tests', value=5, delta='Total Tests: 7')
        # make the title 
        st.markdown("<h5>Task Output </h5>", True)

        # make a copy of the data and make a new column for task completion
        # taskscompleted = roles[["StudentName", "Responsibilities", "Description"]].rename({"Responsibilities": "Role"}, axis=1).copy()
        # insert the data in the UI
        st.dataframe(taskscompleted, hide_index=True, use_container_width=True, height=500)

        st.write(
        """
        <style>
        [data-testid="stMetricDelta"] svg {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # call the second column and continue the design under
    with sections[1]:
        # st.markdown("<h5>❗ Issues Information </h5>", True)

        # Set 

        # insert the container of all issue alerts, height of container=500
        issuesinfo(height=500, in_container=True)