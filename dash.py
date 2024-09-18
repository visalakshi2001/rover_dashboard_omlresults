import streamlit as st
import pandas as pd
import numpy as np
import os

import plotly.express as px
import plotly.graph_objects as go

def dashboard():

    colors = px.colors.qualitative.Plotly

    cur_dir = os.path.abspath(os.getcwd())

    reqs = pd.read_csv(os.path.join("reports", "Requirements.csv"), index_col=0)
    task = pd.read_csv(os.path.join("reports", "Tasks.csv"), index_col=0)
    test = pd.read_csv(os.path.join("reports", "Tests.csv"), index_col=0)

    reqdata = {
        "RequirementName": reqs["ReqName"].values.tolist(),
        "ReqID": reqs["ReqID"].values.tolist(),
        'Satisfied': [0, 0, 0, 0, 0, 0, 1],
        'Verified': [0, 0, 0, 1, 0, 0, 1],
        'Pending': [1, 1, 1, 0, 1, 1, 0]
    }

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

    topcols = st.columns([1, 1.5])

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FIGURE 1 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    with topcols[0]:    
        st.plotly_chart(fig1, use_container_width=True)
    
    task['Start'] = pd.date_range(start='2023-01-01', periods=len(task), freq='M')
    task['Finish'] = task['Start'] + pd.Timedelta(days=30)

    fig2 = px.timeline(task, x_start="Start", x_end="Finish", y="Description", color="StudentName", title='Task Timeline')
    fig2.update_layout(legend=dict(xanchor="left", x=0, y=1, yanchor="bottom", orientation="h"))
    fig2.update_yaxes(tickfont_size=16, tickfont_color="black")
    fig2.update_xaxes(tickfont_size=16, tickfont_color="black")

    with topcols[1]:    
        st.plotly_chart(fig2, use_container_width=True)

    task["Outputs"] = task["Outputs"].str.split(', ')
    task = task.explode('Outputs')
    task["CompletionStatus"] = np.where(pd.notnull(task["Outputs"]), "Completed", "Not Completed")
    
    fig3 = px.bar(task, y="StudentName", color="CompletionStatus", orientation="h",
                  text="Outputs", title="Tasks Assigned to Each Student", 
                  custom_data="Description",
                  color_discrete_map= {"Completed": colors[0], "Not Completed": colors[1]},
                  labels={'x': 'Student', 'y': 'Number of Tasks'})

    fig3.update_traces(textposition="inside", hovertemplate="%{customdata}", textfont_size=16)
    fig3.update_yaxes(tickfont_size=16, tickfont_color="black")
    # fig3.update_layout(legend=dict(xanchor="left", yanchor="bottom"))

    st.plotly_chart(fig3, use_container_width=True)


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FIGURE 2 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    middlecols = st.columns(2)

    test['Completed'] = pd.notnull(test['TestOutput'])
    fig4 = px.pie(test, names='Completed', title='Test Completion Status', 
                  labels={'Completed': 'Completed (True/False)'}, color_discrete_sequence=[colors[1], colors[0]])

    task['HasOutput'] = pd.notnull(task['Outputs'])
    fig5 = px.pie(task, names='HasOutput', title='Task Completion Status', 
                  labels={'HasOutput': 'Completed (True/False)'}, color_discrete_sequence=[colors[0], colors[1]])

    with middlecols[1]:
        st.plotly_chart(fig4, use_container_width=True)

    with middlecols[0]:
        st.plotly_chart(fig5, use_container_width=True)


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FIGURE 3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    bottomcols = st.columns(2)

    task['HasOutput'] = pd.notnull(task['Outputs'])
    fig6 = px.scatter(task, x='TaskID', y='HasOutput', 
                      title='Tasks vs Outputs', custom_data=["StudentName", "Description"])
    
    fig6.update_traces(hovertemplate="Student: %{customdata[0]} <br> Task: %{customdata[1]} <br> CompletedWithOutput: %{y}")
    
    with bottomcols[0]:
        st.plotly_chart(fig6, use_container_width=True)

    # Creating the treemap
    labels = []
    parents = []
    hovertexts = []

    # Add requirements
    labels.extend(reqs["ReqName"].to_list())
    parents.extend(["" for req in reqs["ReqName"]])
    hovertexts.extend(reqs["ReqText"])

    # Add tasks
    for i,t in enumerate(task["Outputs"]):
        if t in reqs["ReqName"].to_list():
            labels.append(task["Description"].iloc[i])
            parents.append(t)
            hovertexts.append(f"Task: {task['Description'].iloc[i]}<br>ReqText: {reqs['ReqText'].iloc[reqs['ReqName'].to_list().index(t)]}")

    
    # Add tests
    for i,t in test.iterrows():
        for j,r in reqs.iterrows():
            if r["VerifiedName"] == t["Test"]:
                labels.append(t["Test"])
                parents.append(r["ReqName"])
                hovertexts.append(f"Test: {t['Test']}<br>ReqText: {r['ReqText']}")

    fig7 = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        hovertext=hovertexts,
        hoverinfo="text"
    ))

    fig7.update_layout(title="Tasks and Tests Mapped to Requirements Treemap")

    with bottomcols[1]:
        st.plotly_chart(fig7, use_container_width=True)

    # st.dataframe(reqs)
    # st.dataframe(task)
    # st.dataframe(test)




    # import networkx as nx
    # import plotly.graph_objects as go

    # # Create a network graph for tasks and requirements
    # G1 = nx.Graph()

    # # Adding nodes for tasks and requirements
    # for idx, row in tasks.iterrows():
    #     G1.add_node(row['TaskID'], label=row['Description'], type='task')
        
    # for idx, row in requirements.iterrows():
    #     G1.add_node(row['ReqID'], label=row['ReqText'], type='requirement')

    # # Adding edges based on the outputs of tasks addressing specific requirements
    # task_requirement_relations = {
    #     8: [1, 2, 3, 4, 5, 6, 7], # Task 8 defines all requirements
    #     7: [7] # Task 7 is related to mass requirement
    # }
    # for task, reqs in task_requirement_relations.items():
    #     for req in reqs:
    #         G1.add_edge(task, req)

    # # Create a network graph for requirements and tests
    # G2 = nx.Graph()

    # # Adding nodes for requirements and tests
    # for idx, row in requirements.iterrows():
    #     G2.add_node(row['ReqID'], label=row['ReqText'], type='requirement')

    # for idx, row in tests.iterrows():
    #     G2.add_node(row['Test'], label=row['Test'], type='test')

    # # Adding edges based on the tests verifying specific requirements
    # for idx, row in tests.iterrows():
    #     if row['VerifiesRequirement']:
    #         req_id = requirements[requirements['ReqName'] == row['VerifiesRequirement']].index[0] + 1
    #         G2.add_edge(row['Test'], req_id)

    # # Create a comprehensive network graph for tasks, requirements, and tests
    # G3 = nx.Graph()

    # # Adding nodes for tasks, requirements, and tests
    # for idx, row in tasks.iterrows():
    #     G3.add_node(row['TaskID'], label=row['Description'], type='task')

    # for idx, row in requirements.iterrows():
    #     G3.add_node(row['ReqID'], label=row['ReqText'], type='requirement')

    # for idx, row in tests.iterrows():
    #     G3.add_node(row['Test'], label=row['Test'], type='test')

    # # Adding edges for task-requirement and requirement-test relationships
    # for task, reqs in task_requirement_relations.items():
    #     for req in reqs:
    #         G3.add_edge(task, req)

    # for idx, row in tests.iterrows():
    #     if row['VerifiesRequirement']:
    #         req_id = requirements[requirements['ReqName'] == row['VerifiesRequirement']].index[0] + 1
    #         G3.add_edge(row['Test'], req_id)

    # # Helper function to create Plotly edge traces
    # def create_edge_trace(G):
    #     edge_x = []
    #     edge_y = []
    #     for edge in G.edges():
    #         x0, y0 = G.nodes[edge[0]]['pos']
    #         x1, y1 = G.nodes[edge[1]]['pos']
    #         edge_x.extend([x0, x1, None])
    #         edge_y.extend([y0, y1, None])
    #     edge_trace = go.Scatter(
    #         x=edge_x, y=edge_y,
    #         line=dict(width=0.5, color='#888'),
    #         hoverinfo='none',
    #         mode='lines')
    #     return edge_trace

    # # Helper function to create Plotly node traces
    # def create_node_trace(G):
    #     node_x = []
    #     node_y = []
    #     labels = []
    #     node_types = []
    #     for node in G.nodes():
    #         x, y = G.nodes[node]['pos']
    #         node_x.append(x)
    #         node_y.append(y)
    #         labels.append(G.nodes[node]['label'])
    #         node_types.append(G.nodes[node]['type'])
    #     node_trace = go.Scatter(
    #         x=node_x, y=node_y,
    #         mode='markers+text',
    #         text=labels,
    #         textposition='top center',
    #         hoverinfo='text',
    #         marker=dict(
    #             showscale=True,
    #             colorscale='YlGnBu',
    #             size=10,
    #             color=[{'task': 0, 'requirement': 1, 'test': 2}[type_] for type_ in node_types],
    #             colorbar=dict(
    #                 thickness=15,
    #                 title='Node Type',
    #                 xanchor='left',
    #                 titleside='right'
    #             ),
    #             line_width=2))
    #     return node_trace

    # # Position nodes using networkx's spring layout
    # for G in [G1, G2, G3]:
    #     pos = nx.spring_layout(G)
    #     for node in G.nodes:
    #         G.nodes[node]['pos'] = pos[node]

    # # Create Plotly traces for each network graph
    # edge_trace1 = create_edge_trace(G1)
    # node_trace1 = create_node_trace(G1)

    # edge_trace2 = create_edge_trace(G2)
    # node_trace2 = create_node_trace(G2)

    # edge_trace3 = create_edge_trace(G3)
    # node_trace3 = create_node_trace(G3)

    # # Create the figures
    # fig1 = go.Figure(data=[edge_trace1, node_trace1],
    #                 layout=go.Layout(
    #                     title='Network Graph: Tasks and Requirements',
    #                     showlegend=False,
    #                     hovermode='closest',
    #                     margin=dict(b=20,l=5,r=5,t=40),
    #                     xaxis=dict(showgrid=False, zeroline=False),
    #                     yaxis=dict(showgrid=False, zeroline=False)))

    # fig2 = go.Figure(data=[edge_trace2, node_trace2],
    #                 layout=go.Layout(
    #                     title='Network Graph: Requirements and Tests',
    #                     showlegend=False,
    #                     hovermode='closest',
    #                     margin=dict(b=20,l=5,r=5,t=40),
    #                     xaxis=dict(showgrid=False, zeroline=False),
    #                     yaxis=dict(showgrid=False, zeroline=False)))

    # fig3 = go.Figure(data=[edge_trace3, node_trace3],
    #                 layout=go.Layout(
    #                  title='Network Graph: Tasks, Requirements, and Tests',
    #                  showlegend=False,
    #                  hovermode='closest',
    #                  margin=dict(b=20,l=5,r=5,t=40),
    #                  xaxis=dict(showgrid=False, zeroline=False),
    #                  yaxis=dict(showgrid=False, zeroline=False)))


def tne():
    colors = px.colors.qualitative.Plotly

    keycap = pd.read_csv(os.path.join("reports", "Query5_KeyCapabilities 1.csv"), index_col=0)
    schdata = pd.read_csv(os.path.join("reports", "Query6_Scheduling 1.csv"), index_col=0)

    topcols = st.columns([1,1])

    with topcols[0]:
    
        metriccols = st.columns(3)

        with metriccols[0]:
            for idx,row in keycap.iterrows():
                if idx % 3 == 0:
                    st.metric(label=row["KCName"] + " (" + row["SatisfiedBy"] + ")", value=str(row["Threshold"]) + " " + row["Unit"], 
                            delta="Target:" + " " + str(row["Objective"]) + " " + row["Unit"], delta_color="off"
                            # delta_color="normal" if row["Objective"] < row["Threshold"] else "inverse"
                            )
        
        with metriccols[1]:
            for idx,row in keycap.iterrows():
                if idx % 3 == 1:
                    st.metric(label=row["KCName"] + " (" + row["SatisfiedBy"] + ")", value=str(row["Threshold"]) + " " + row["Unit"], 
                            delta="Target:" + " " + str(row["Objective"]) + " " + row["Unit"], delta_color="off"
                            # delta_color="normal" if row["Objective"] < row["Threshold"] else "inverse"
                            )
        
        with metriccols[2]:
            for idx,row in keycap.iterrows():
                if idx % 3 == 2:
                    st.metric(label=row["KCName"] + " (" + row["SatisfiedBy"] + ")", value=str(row["Threshold"]) + " " + row["Unit"], 
                            delta="Target:" + " " + str(row["Objective"]) + " " + row["Unit"], delta_color="off"
                            # delta_color="normal" if row["Objective"] < row["Threshold"] else "inverse"
                            )
                
        st.write(
                """
                <style>
                [data-testid="stMetricDelta"] svg {
                    display: none;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
    
    with topcols[1]:
        keycap["newObj"] = np.where(keycap["Objective"] > 100, keycap["Objective"]/100, keycap["Objective"])
        keycap["newThr"] = np.where(keycap["Threshold"] > 100, keycap["Threshold"]/100, keycap["Threshold"])
        fig0 = go.Figure(data=[
            go.Bar(name='Objective', y=keycap["KCName"] + " " + keycap["SatisfiedBy"], x=keycap["newObj"], 
                orientation="h", marker=dict(color=colors[1], opacity=0.5), customdata=keycap["VerificationMethodName"], hovertemplate=" %{customdata} ",
                ),
            go.Bar(name='Threshold', y=keycap["KCName"] + " " + keycap["SatisfiedBy"], x=keycap["newThr"],
                orientation="h", marker=dict(color=colors[2], opacity=0.5), customdata=keycap["VerificationMethodName"], hovertemplate="Verified by %{customdata} ",
                )
        ])

        annotations = []
        for xd, yd, xdn in zip(keycap["newObj"], keycap["KCName"] + " " + keycap["SatisfiedBy"], keycap["Objective"]):
            annotations.append(dict(xref="x1", yref="y1",
                                    x = xd + 8, y = yd,
                                    text= str(xdn), showarrow=False,
                                    font_color = colors[1],
                                    font_size=16))
        for xd, yd, xdn in zip(keycap["newThr"], keycap["KCName"] + " " + keycap["SatisfiedBy"], keycap["Threshold"]):
            annotations.append(dict(xref="x1", yref="y1",
                                    x = xd, y = yd,
                                    text= str(xdn), showarrow=False,
                                    font_color = "black"
                                    ))

        fig0.update_layout(barmode='overlay', title='Key capacities fulfilled', annotations=annotations,
                           xaxis=dict(visible=False))
        fig0.update_traces(width=0.7)
        fig0.update_yaxes(tickfont_size=14, tickfont_color="black")

        st.plotly_chart(fig0, use_container_width=True)

    middlecols = st.columns([1.5, 0.5])

    with middlecols[0]:
        schdata["Site"] = np.where(pd.isnull(schdata["Site"]), "None", schdata["Site"])
        fig1 = px.bar(schdata, y="TestSubjects", orientation="h", color="Site",
                    text="VMName", title="Allocated resources (VM) to Subjects", 
                    custom_data="VMName")

        fig1.update_traces(textposition="inside", hovertemplate="%{customdata}", textfont_size=16)
        fig1.update_yaxes(tickfont_size=16, tickfont_color="black")
        fig1.update_layout(legend=dict(xanchor="left", yanchor="bottom", x=0, y=1, orientation="h"))

        st.plotly_chart(fig1, use_container_width=True)

    with middlecols[1]:
        site_counts = schdata["Site"].value_counts().reset_index()
        site_counts.columns = ["Site", "Count"]
        fig2 = px.pie(site_counts, names="Site", values="Count", title="Distribution of Tests per Site")

        st.plotly_chart(fig2, use_container_width=True)

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

    # print(schdata["End"])

    # # Sunburst Chart of Test Distribution by Site and Test Type
    # sunburst_data = schdata[pd.notnull(schdata['Site'])]
    # fig4 = px.sunburst(sunburst_data, path=['Site', 'VMName'], title="Test Distribution by Site and Test Type")

    # fig4.update_traces(textfont_size=16)
    # st.plotly_chart(fig4, use_container_width=True)