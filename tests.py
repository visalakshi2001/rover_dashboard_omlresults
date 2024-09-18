import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go

from issues import issuesinfo

colors = px.colors.qualitative.Plotly

def testschedule():
    test = pd.read_csv(os.path.join("reports", "Tests.csv"), index_col=0)
    schdata = pd.read_csv(os.path.join("reports", "Query6_Scheduling 1.csv"), index_col=0)
    top = st.columns([0.3, 0.3, 0.4])

    with top[0]:
        test['Completed'] = pd.notnull(test['TestOutput'])
        fig = px.pie(test, names='Completed', title='Test Completion Status', 
                  labels={'Completed': 'Completed (True/False)'}, color_discrete_sequence=[colors[1], colors[0]])
        st.plotly_chart(fig, True)
    
    with top[1]:    
        schdata['Scheduled'] = (pd.notnull(schdata['Start']) | pd.notnull(schdata["End"]))
        fig = px.pie(schdata, names='Scheduled', title='Test Scheduling Status', 
                    labels={'Scheduled': 'Scheduled (True/False)'}, color_discrete_sequence=[colors[2], colors[0]])
        st.plotly_chart(fig, True)

    with top[2]:
        issuesinfo()    
    
    sch_opts = ["Test Schedule", "Milestone Schedule"]
    schedule_choice = st.selectbox("Select a schedule to view", options=["Test Schedule", "Milestone Schedule"])

    if schedule_choice == sch_opts[0]:
        st.write("Test")
    
    if schedule_choice == sch_opts[1]:
        st.write("Milestone")