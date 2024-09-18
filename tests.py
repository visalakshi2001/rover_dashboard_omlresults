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
        fig3 = px.timeline(schdata, x_start="Start", x_end="End", y="TestSubjects", color="VMName", 
                       title="Test Schedules", custom_data=["Start", "End", "VMName"])
        fig3.update_traces(width=1)

        fig3.add_trace(go.Scatter(name="TimeStamp", x=schdata["End"], y=schdata["TestSubjects"], 
                                mode="markers",
                                marker=dict(
                                    size=10,
                                    ),
                                    # hovertemplate="",
                                    customdata=[schdata["Start"], schdata["End"]],
                                showlegend=False,
                                )
                    )
        fig3.update_traces(hovertemplate="Start: %{customdata[0]} <br> End: %{customdata[1]} <br> VMName: %{customdata[2]}")

        st.plotly_chart(fig3,use_container_width=True)
    
    if schedule_choice == sch_opts[1]:
        decisionreview = pd.read_csv("results/Query3_Decisions.csv", index_col=0)
        decisionreview['ReviewStart'] = pd.to_datetime(decisionreview['ReviewStart'])
        # Define ReviewEnd as 1 hour after ReviewStart (since no end times are given)
        decisionreview['ReviewEnd'] = decisionreview['ReviewStart'] + pd.Timedelta(hours=1)
        # Define a function to extract the week of year
        decisionreview['Week'] = decisionreview['ReviewStart'].dt.strftime('%Y-W%U')

        # Creating the Plotly figure
        fig = px.timeline(decisionreview, x_start="ReviewStart", x_end="ReviewEnd", y="Review", color="Decision", text="Milestone", hover_name="Milestone",
                        category_orders={"Review": sorted(decisionreview['Review'].unique(), key=lambda x: str(x))})

        # Update layout to include a dropdown menu for week selection
        week_options = decisionreview['Week'].unique()

        fig.update_layout(
            title="Review Schedule",
            xaxis_title="Time",
            yaxis_title="Review",
            # xaxis=dict(
            #     tickformat="%d %b %Y\n%H:%M",
            #     # range=[decisionreview['ReviewStart'].min() - pd.Timedelta(days=1), decisionreview['ReviewEnd'].min() + pd.Timedelta(days=6)],
            # ),
            updatemenus=[{
                "buttons": [
                    {
                        "args": [
                            {"xaxis.range": [decisionreview[decisionreview['Week'] == week]['ReviewStart'].min() - pd.Timedelta(days=1), decisionreview[decisionreview['Week'] == week]['ReviewEnd'].max() + pd.Timedelta(days=6)]}
                        ],
                        "label": week,
                        "method": "relayout"
                    }
                    for week in week_options
                ],
                "direction": "down",
                "showactive": True,
                "x": 0.17,
                "xanchor": "left",
                "y": 1.15,
                "yanchor": "top"
            }]
        )
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
            'Satisfied': pd.notnull(reqs["SatisfiedName"]), # [0, 0, 0, 0, 0, 0, 1],
            'Verified': pd.notnull(reqs["VerifiedName"]), # [0, 0, 0, 1, 0, 0, 1],
            'Pending':  reqs[["SatisfiedName", "VerifiedName"]].isnull().all(1), # [1, 1, 1, 0, 1, 1, 0]
            "VerifiedName": reqs["VerifiedName"].values,
            "SatisfiedName": reqs["SatisfiedName"].values,
        }

        # st.dataframe(reqdata)

    with top[1]:
        
        cont = st.container(border=True, height=400)

        cont.markdown("<h5>Related Tests</h5>", True)

        # st.dataframe(schdata)
    
    cont = st.container(border=True)

    cont.markdown("<h5>Verification Results (Tracing)</h5>", True)

    fig1 = go.Figure(data=[
        go.Bar(name='Satisfied', y=reqdata["RequirementName"], x=reqdata["Satisfied"], 
               orientation="h", marker=dict(color=colors[2]), customdata=reqdata["ReqID"], hovertemplate=" %{customdata} "
               ),
        go.Bar(name='Verified', y=reqdata["RequirementName"], x=reqdata["Verified"], 
            orientation="h", marker=dict(color=colors[0]), customdata=reqdata["ReqID"], hovertemplate=" %{customdata} "
            ),
        go.Bar(name='Pending', y=reqdata["RequirementName"], x=reqdata["Pending"], 
            orientation="h", marker=dict(color=colors[1]), customdata=reqdata["ReqID"], hovertemplate=" %{customdata} "
            )
    ])

    fig1.update_layout(barmode='stack', title='Requirements Satisfaction and Verification Status')
    fig1.update_yaxes(tickfont_size=16, tickfont_color="black")
    cont.plotly_chart(fig1)
