# to make frontend components
import streamlit as st
# to read data
import pandas as pd
# to make UML graphs
import graphviz


# ########## REQUIREMENTS VIEW FUNCTION
def requirementview():
    # read the data for requirements
    reqs = pd.read_csv("reports/Requirements.csv", index_col=0)

    # Make a dropdown select menu, with options as all the name of Requirements
    req_choice = st.selectbox("Select a Requirement", options=reqs["ReqName"].sort_values().tolist())

    # make three columns of equal width
    cols = st.columns(3)

    # filter the target requirement from the data of all requirement, using the selected requirement name
    # this comes from the name chosen by the user
    target_req = reqs[reqs["ReqName"] == req_choice]

    # initiate empty diagraph chart
    dot = graphviz.Digraph(comment='Hierarchy', strict=True)

    # call the first column and create the chart below
    with cols[0]:
        for index, row in target_req.iterrows():
            requirement = row['ReqName']
            satisfiedby = row['SatisfiedBy']
            verifiedby = row['VerifiedName']
            
            # Add the function node
            dot.node(requirement)
            
            # Add edge from SuperFunction to Function if SuperFunction exists
            if pd.notna(satisfiedby):
                if satisfiedby not in dot.body:
                    dot.node(satisfiedby, shape='box')
                dot.edge(requirement, satisfiedby, label="satisfied by")
            
            # Add AllocatedTo node and edge if it doesn't already exist
            if pd.notna(verifiedby):
                if verifiedby not in dot.body:
                    dot.node(verifiedby, shape='box')
                dot.edge(requirement, verifiedby, label="verified by system")
        st.graphviz_chart(dot)

    # call the second column and display the target requirement information in a table
    with cols[1]:
        st.dataframe(target_req[["ReqName", "SatisfiedBy", "VerifiedName"]], 
                     hide_index=True, height=100, use_container_width=True)
    
    # call the third column and display additional details on the requirement, 
    # along with warnings if applicable
    with cols[2]:
        # make a container of height 420px
        cont = st.container(border=True, height=420)

        # make a heading
        cont.markdown("<h5>Requirement Details & Satisfaction Status</h5>", True)

        # write the details of the target requirement
        cont.markdown(f"""
        **ReqID:** {target_req["ReqID"].iloc[0]} \n 
        **Requirement Name:** {target_req["ReqName"].iloc[0]} \n
        **Description:** {target_req["ReqText"].iloc[0]} \n
        """, True)

        # check for satisfaction and verification details and raise warning if not fulfilled
        satisfied, verified = False, False
        if pd.notnull(target_req["SatisfiedBy"].iloc[0]):
            cont.markdown(f"**Satisfied By:** {target_req['SatisfiedBy'].iloc[0]} \n", True)
            satisfied = True
        if pd.notnull(target_req["VerifiedName"].iloc[0]):
            cont.markdown(f"**Verified By:** {target_req['VerifiedName'].iloc[0]} \n", True)
            verified = True
        
        # raise warning
        if not satisfied:
            cont.warning('This Requirement is not satisfied by any System', icon="⚠️")
        if not verified:
            cont.warning('This Requirement is not verified by any Test/Activity', icon="⚠️")
        if not (satisfied or verified):
            cont.info("See Test Results OR Grading Wizard for all warnings/issues")
        


