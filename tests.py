import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go

from issues import issuesinfo
from plots import scheduletimeline, schedulereviewmilestone

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
        fig = scheduletimeline()
        st.plotly_chart(fig ,use_container_width=True)
        # st.dataframe(pd.read_csv("results/Query6_Scheduling copy.csv", index_col=0), hide_index=True, use_container_width=True)
    
    if schedule_choice == sch_opts[1]:
        fig = schedulereviewmilestone()
        st.plotly_chart(fig, True)

def testresults():

    top = st.columns(2)

    with top[0]:
        test = pd.read_csv(os.path.join("reports", "Tests.csv"), index_col=0)
        schdata = pd.read_csv(os.path.join("reports", "Query6_Scheduling 1.csv"), index_col=0)
        reqs = pd.read_csv(os.path.join("reports", "Requirements.csv"), index_col=0)


        test_choices = st.selectbox("Select a test to view details", options=schdata["VMName"].values.tolist())
        st.write("Values related to test will be displayed here")
        
        reqdata = {
            "RequirementName": reqs["ReqName"].values.tolist(),
            "ReqID": reqs["ReqID"].values.tolist(),
            'Satisfied': pd.notnull(reqs["SatisfiedBy"]), # [0, 0, 0, 0, 0, 0, 1],
            'Verified': pd.notnull(reqs["VerifiedName"]), # [0, 0, 0, 1, 0, 0, 1],
            'Pending':  reqs[["SatisfiedBy", "VerifiedName"]].isnull().all(1), # [1, 1, 1, 0, 1, 1, 0]
            "VerifiedName": reqs["VerifiedName"].values,
            "SatisfiedName": reqs["SatisfiedBy"].values,
        }


    with top[1]:
        
        cont = st.container(border=True, height=400)

        cont.markdown("<h5>Related Tests</h5>", True)
    
    cont = st.container(border=True)

    cont.markdown("<h5>Verification Results (Tracing)</h5>", True)

    