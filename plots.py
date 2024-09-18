import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


def scheduletimeline():

    testscheduling = pd.read_csv("results/Query6_Scheduling copy.csv", index_col=0)

    testscheduling = testscheduling[testscheduling["Include"] == True].copy()
    testscheduling["Start"] = pd.to_datetime(testscheduling["Start"])
    testscheduling["End"] = pd.to_datetime(testscheduling["End"])

    # Define a function to extract the week of year
    testscheduling['Week'] = testscheduling['Start'].dt.strftime('%Y-W%U')

    # Creating the Plotly figure
    fig = px.timeline(testscheduling, x_start="Start", x_end="End", y="TestSubjects", color="VMName", text="VMName", hover_name="VM",
                    category_orders={"Site": sorted(testscheduling['Site'].unique(), key=lambda x: str(x))})

    
    # Update layout to include a dropdown menu for week selection
    week_options = testscheduling['Week'].unique()

    fig.update_layout(
        title="Test Schedule",
        xaxis_title="Time",
        yaxis_title="Test Site",
        xaxis=dict(
            tickformat="%d %b %Y\n%H:%M",
            range=[testscheduling['Start'].min() - pd.Timedelta(days=1), testscheduling['End'].min() + pd.Timedelta(days=6)],
        ),
        updatemenus=[{
            "buttons": [
                {
                    "args": [
                        {"xaxis.range": [testscheduling[testscheduling['Week'] == week]['Start'].min() - pd.Timedelta(days=1), testscheduling[testscheduling['Week'] == week]['End'].max() + pd.Timedelta(days=6)]}
                    ],
                    "label": week,
                    "method": "relayout"
                }
                for week in week_options
            ],
            "direction": "down",
            "showactive": True,
            "x": 0.17,
            "xanchor": "center",
            "y": 1.15,
            "yanchor": "bottom"
        }],
        legend=dict(xanchor="left", x=0, y=1, yanchor="bottom", orientation="h")
    )
    vlinedate = datetime.today().date()
    fig.add_vline(x=datetime(vlinedate.year, vlinedate.month, vlinedate.day).timestamp() * 1000, annotation_text= f"today {vlinedate.month}/{vlinedate.day}")
    
    return fig

def schedulereviewmilestone():
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
    
    return fig