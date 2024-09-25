import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go
import graphviz

from issues import issuesinfo
from plots import scheduletimeline, schedulereviewmilestone

colors = px.colors.qualitative.Plotly

def testschedule():
    test = pd.read_csv(os.path.join("reports", "Tests.csv"), index_col=0)
    schdata = pd.read_csv(os.path.join("results", "Query6_Scheduling copy.csv"), index_col=0)
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
        issuesinfo(400)    
    
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
        schtests = pd.read_csv(os.path.join("results", "Query6_Scheduling copy.csv"), index_col=0)
        reqs = pd.read_csv("reports/Requirements.csv", index_col=0)
        checks = pd.read_csv("results/Query7_VerificationCheck.csv", index_col=0)

        test_choice = st.selectbox("Select a test to view details", options=schtests[schtests["Include"] == True]["VMName"].values.tolist())
        target_test = test[test["Test"] == test_choice]

        st.markdown(f"**Test Name:** {target_test['Test'].iloc[0]} \n", True)

        scheduled, verified = False, False
        verreq = target_test["VerifiesRequirement"].iloc[0]
        testsite = schtests[schtests['VMName'] == test_choice]['Site'].iloc[0]
        if pd.notnull(verreq):
            st.markdown(f"**Requirement Name:** {reqs[reqs['ReqID'].str.endswith(verreq)]['ReqName'].iloc[0]} \n", True)
            st.markdown(f"**Requirement ID:** {reqs[reqs['ReqID'].str.endswith(verreq)]['ReqID'].iloc[0]} \n", True)
            verified = True
        
        if pd.notnull(testsite):
                st.markdown(f"**Test Site:** {testsite} \n", True)
                scheduled = True
        
        if not verified:
            st.warning('This Test does not verify Requirement', icon="⚠️")
        if not scheduled:
            st.error('This Test does not have any Test Site/Environment', icon="❗")
        if not (verified and scheduled):
            st.info("See Test Results OR Grading Wizard for all warnings/issues")

    
    dot = graphviz.Digraph(comment='Hierarchy', strict=True)

    with top[1]:
        st.markdown("<h5>🛰️ Test Result Verification Analysis</h5>", True)
        target_test = test[test["Test"] == test_choice]
        for index, row in target_test.iterrows():
            test = row['Test']
            testsubject = row['TestSubject']
            output = row['TestOutput']
            verreq = row["VerifiesRequirement"]
            
            # Add the function node
            dot.node(test)
            
            # Add edge from SuperFunction to Function if SuperFunction exists
            if pd.notna(testsubject):
                if testsubject not in dot.body:
                    dot.node(testsubject)
                dot.edge(test, testsubject, label="has test-subject")
            
            # Add AllocatedTo node and edge if it doesn't already exist
            if pd.notna(output):
                dot.edge(test, output, label="has output")
                target_check = checks[checks["TestName"] == test_choice]
                if not target_check.empty:
                    if pd.isnull(target_check["Unit"].iloc[0]): target_check["Unit"].iloc[0] = ""
                    check_node = target_check["Value"].iloc[0] + target_check["Unit"].iloc[0]
                    dot.node(check_node, shape="box")
                    dot.edge(output, check_node, label="has output value")

            if pd.notna(verreq):
                if verreq not in dot.body:
                    dot.node(verreq, shape="box")
                dot.edge(test, verreq, label="verifies requirement")
        cont = st.container(border=True)
        cont.graphviz_chart(dot)
    

    bottom = st.columns(2)


    with bottom[0]:
        checks = pd.read_csv("results/Query7_VerificationCheck.csv", index_col=0)

        subcols_bt = st.columns(2)
        target_check = checks[checks["TestName"] == test_choice]

        with subcols_bt[0]:
            for i,row in target_check.iterrows():
                if row["Value"] > row["MinMaxValue"] or row["Value"] == row["MinMaxValue"]:
                    delta_color = "normal"
                else: delta_color = "inverse"
                if pd.isnull(row["Unit"]): row["Unit"] = ""

                if test_choice == "Mass Test":
                    st.metric(label=row["TestMeasurement"], 
                            value=row["Value"] + row["Unit"], 
                            delta="Max-Value: " + row["MinMaxValue"] + row["Unit"], 
                            delta_color=delta_color)
                else:
                    st.metric(label=row["TestMeasurement"], 
                            value=row["Value"] + row["Unit"], 
                            delta="Min-Value: " + row["MinMaxValue"] + row["Unit"], 
                            delta_color=delta_color)
        if target_check.empty == True:
            st.warning(f"{test_choice} does not have any verification results yet", icon="⚠️")

        with subcols_bt[1]:
            pass
    