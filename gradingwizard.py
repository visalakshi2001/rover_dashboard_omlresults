import streamlit as st
import pandas as pd

from issues import issuesinfo

def gradingtaskcompletion():
    roles = pd.read_csv("reports/Tasks_Rover.csv", index_col=0)

    sections = st.columns([0.6, 0.4])

    with sections[0]:
        st.markdown("<h5>✅ Task Output </h5>", True)

        taskscompleted = roles[["StudentName", "Role", "Description"]].copy()
        taskscompleted["Completed"] = pd.notnull(roles["Outputs"])
        st.dataframe(taskscompleted, hide_index=True, use_container_width=True, height=500)
    
    with sections[1]:
        st.markdown("<h5>❗ Issues Information </h5>", True)
        issuesinfo()