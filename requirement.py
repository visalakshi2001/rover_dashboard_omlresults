import streamlit as st
import pandas as pd
import numpy as np
import graphviz
import plotly.express as px
import plotly.graph_objects as go

def requirementview():


    reqs = pd.read_csv("reports/Requirements.csv", index_col=0)

    req_choice = st.selectbox("Select a Requirement", options=reqs["ReqName"].values.tolist())

    top = st.columns(2)
    bottom = st.columns(3)

    target_req = reqs[reqs["ReqName"] == req_choice]
    dot = graphviz.Digraph(comment='Hierarchy', strict=True)

    with bottom[0]:
        for index, row in target_req.iterrows():
            requirement = row['ReqName']
            satisfiedby = row['SatisfiedBy']
            verifiedby = row['VerifiedName']
            
            # Add the function node
            dot.node(requirement)
            
            # Add edge from SuperFunction to Function if SuperFunction exists
            if pd.notna(satisfiedby):
                dot.edge(requirement, satisfiedby, label="satisfied by")
            
            # Add AllocatedTo node and edge if it doesn't already exist
            if pd.notna(verifiedby):
                if verifiedby not in dot.body:
                    dot.node(verifiedby, shape='box')
                dot.edge(satisfiedby, verifiedby, label="verified by system")
        st.graphviz_chart(dot)
    with bottom[1]:
        st.dataframe(target_req[["ReqName", "SatisfiedBy", "VerifiedName"]], 
                     hide_index=True, height=100, use_container_width=True)
    
    with bottom[2]:
        cont = st.container(border=True, height=420)

        cont.markdown("<h5>Requirement Details & Satisfaction Status</h5>", True)

        cont.markdown(f"""
        **ReqID:** {target_req["ReqID"].iloc[0]} \n 
        **Requirement Name:** {target_req["ReqName"].iloc[0]} \n
        **Description:** {target_req["ReqText"].iloc[0]} \n
        """, True)

        satisfied, verified = False, False
        if pd.notnull(target_req["SatisfiedBy"].iloc[0]):
            cont.markdown(f"**Satisfied By:** {target_req['SatisfiedBy'].iloc[0]} \n", True)
            satisfied = True
        if pd.notnull(target_req["VerifiedName"].iloc[0]):
            cont.markdown(f"**Verified By:** {target_req['VerifiedName'].iloc[0]} \n", True)
            verified = True
        
        if not satisfied:
            cont.warning('This Requirement is not satisfied by any Test', icon="⚠️")
        if not verified:
            cont.warning('This Requirement is not verified by any Simulation/Output', icon="⚠️")
        if not (satisfied or verified):
            cont.info("See Test Results OR Grading Wizard for all warnings/issues")
        


