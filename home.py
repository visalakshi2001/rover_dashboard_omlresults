# To make components
import streamlit as st
# To read CSV files
import pandas as pd
# to handle datetime values 
from datetime import datetime
# To make the plots, charts and graphs
import plotly.express as px


colors = px.colors.qualitative.Plotly

# ########## HOME VIEW FUNCTION
def homefunc():
    # read the data for the assigned tasks
    roles = pd.read_csv("reports/Tasks_Rover.csv", index_col=0)
    roles['HasOutput'] = pd.notnull(roles['Outputs'])
    
    # make two columns of sizes 40% and 60%
    sections = st.columns([0.4, 0.6])

    # call the first column and design the view under
    with sections[0]:
        # Add title of the column
        st.markdown("<h5>Project Overview</h5>", True)
        st.markdown(f"**Today:** {datetime.today().date().strftime('%A %B %d, %Y')}", True)

        # Add each content using st.metric()
        st.metric(label="**🛰️ Project Name**", value="Rover Design Exercise")
        st.metric(label="**🛰️ Group Name**", value="Group 1")
        st.metric(label="**🛰️ Submission Date**", value=datetime.strptime("2024-09-13", "%Y-%m-%d").date().strftime("%A, %B %d %Y"))

        st.divider()

        # Add second title in the column
        st.markdown("<h5>Project Summary</h5>", True)

        # Create two sub-columns of equal sizes
        left, right = st.columns(2)
        # Add each content using column_object.metric()
        left.metric(label="**🛰️ No. of Requirements**", value=7)
        left.metric(label="**🛰️ No. of Components**", value=15)
        left.metric(label="**🛰️ No. of Tools integrated**", value=4, delta="SysML v2, Jama, Jira, GitHub")
        right.metric(label="**🛰️ No. of Tasks**", value=11)
        right.metric(label="**🛰️ No. of Complete Tasks**", value=4)


    # call the second column and design the view under
    with sections[1]:
        # Add the title for the column
        st.markdown("<h5>Group Summary</h5>", True)

        # Add the roles using st.dataframe()
        st.markdown("<h6>🛰️ Assigned Roles</h6>", True)
        st.dataframe(roles[["StudentName", "Responsibilities"]].rename({"Responsibilities": "Role"}, axis=1).drop_duplicates(), hide_index=True, use_container_width=True)

        # st.divider()

        # Add the second title in column 
        st.markdown("<h6>🛰️ Assigned Tasks</h6>", True)
        
        # Add the tasks, with colored rows for pending outputs
        st.write("_Fields marked in :orange[yellow] are pending tasks_")
        st.dataframe(roles[["StudentName", "Description", "Outputs"]].style. \
                       apply(lambda x: ["background-color: rgb(244 215 60);"]*len(x) if pd.isnull(x.Outputs) else None, axis=1), 
                       
                       hide_index=True, use_container_width=True)


