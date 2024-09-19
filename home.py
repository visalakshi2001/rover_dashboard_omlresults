import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

colors = px.colors.qualitative.Plotly

def homefunc():
    sections = st.columns([0.4, 0.6])
    roles = pd.read_csv("reports/Tasks_Rover.csv", index_col=0)
    roles['HasOutput'] = pd.notnull(roles['Outputs'])
    

    with sections[0]:

        # top = st.container(border=True, height=400)
        # bottom = st.container(border=True,)
        
        st.markdown("<h5>Project Overview</h5>", True)
        st.markdown(f"**Today:** {datetime.today().date().strftime('%A %B %d, %Y')}", True)

        st.metric(label="**🛰️ Project Name**", value="Rover Design Exercise")
        st.metric(label="**🛰️ Group Name**", value="Group 1")
        st.metric(label="**🛰️ Submission Date**", value=datetime.strptime("2024-09-13", "%Y-%m-%d").date().strftime("%A, %B %d %Y"))


        # fig = px.pie(roles, names='HasOutput', title='Task Completion Status', 
        #           labels={'HasOutput': 'Completed (True/False)'}, color_discrete_sequence=[colors[0], colors[1]],
        #           height=280, width=400)

        # top.plotly_chart(fig)

        st.divider()

        st.markdown("<h5>Project Summary</h5>", True)
        left, right = st.columns(2)

        left.metric(label="**🛰️ No. of Requirements**", value=6)
        left.metric(label="**🛰️ No. of Components**", value=15)
        left.metric(label="**🛰️ No. of Tools integrated**", value=4, delta="SysML v2, Jama, Jira, GitHub")
        right.metric(label="**🛰️ No. of Tasks**", value=10)
        right.metric(label="**🛰️ No. of Complete Tasks**", value=8)

    with sections[1]:
        st.markdown("<h5>Group Summary</h5>", True)

        st.markdown("<h6>🛰️ Assigned Roles</h6>", True)
        st.dataframe(roles[["StudentName", "Responsibilities"]].rename({"Responsibilities": "Role"}, axis=1).drop_duplicates(), hide_index=True, use_container_width=True)

        # st.divider()

        st.markdown("<h6>🛰️ Assigned Tasks</h6>", True)
        st.write("_Fields marked in :orange[yellow] are pending tasks_")
        st.dataframe(roles[["StudentName", "Description", "Outputs"]].style. \
                       apply(lambda x: ["background-color: rgb(244 215 60);"]*len(x) if pd.isnull(x.Outputs) else None, axis=1), 
                       
                       hide_index=True, use_container_width=True)


