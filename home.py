import streamlit as st
import pandas as pd


def homefunc():
    sections = st.columns([0.4, 0.6])

    with sections[0]:
        top = st.container(border=True, height=400)
        bottom = st.container(border=True, height=400)

        top.markdown("<h5>Project Overview</h5>", True)

        top.write("Project Name: Rover Design Exercise")
        top.write("Group Name: Group 1")
        top.write("Submission Date: September 13th, 2024")

        bottom.markdown("<h5>Project Summary</h5>", True)

        bottom.write("No. of Requirements: 6")
        bottom.write("No. of Componenets: ")
        bottom.write("No of tooles integrated:  SysMLv2, Jira, Jama ")

    with sections[1]:
        cont = st.container(border=True, height=800)

        cont.markdown("<h5>Group Summary</h5>", True)

        roles = pd.read_csv("reports/Tasks.csv", index_col=0)
        role_dict = dict(zip(roles["StudentName"].value_counts().index, 
                         ["Test Engineer", "Test Engineer", "Systems Architect", "Program Manager", "Software Engineer", "CBTDEV", "Test Engineer"]))
        roles["Role"] = roles["StudentName"].apply(lambda x: role_dict[x])

        # roles["Completed"] = ["True", "True", "False", "True", "True", "True"]

        cont.dataframe(roles[["StudentName", "Role"]].drop_duplicates(), use_container_width=True)

        cont.dataframe(roles[["StudentName", "Description"]], use_container_width=True)


