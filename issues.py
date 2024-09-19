import streamlit as st
import pandas as pd
from itertools import combinations

def sysissues():

    top_cols = st.columns(3)

    with top_cols[0]:
        conflicts = st.expander("⚠️ Four tests have overlapping schedule", expanded=True)

        with conflicts:
            with st.container(border=True):
                st.error("Pathway Creation Time Test has potential schedule conflict with other tests", icon="❗")
                st.markdown("<li>Test Names: Maneuvrability Test</li> \
                            <li>Scheduled Date and Time: September 1 12:00 - 13:00</li>  \
                            <li>Conflict Type: Has the same Site TE53_Environment</li>  \
                            ",True)
            with st.container(border=True):
                st.error("Maneuvrability Test has potential schedule conflict with other tests", icon="❗")
                st.markdown("<li>Test Names: Pathway Creation Time</li> \
                            <li>Scheduled Date and Time: September 1 12:00 - 13:00</li>  \
                            <li>Conflict Type: Has the same Site TE53_Environment</li>  \
                            ",True)
            with st.container(border=True):
                st.error("Path Confidence Test has potential schedule conflict with other tests", icon="❗")
                st.markdown("<li>Test Names: Information Loss Test</li> \
                            <li>Scheduled Date and Time: September 2 12:00 - 13:00</li>  \
                            <li>Conflict Type: Has the same Equipment LSNDS</li>  \
                            ",True)
            with st.container(border=True):
                st.error("Information Loss Test has potential schedule conflict with other tests", icon="❗")
                st.markdown("<li>Test Names: Path Confidence Test</li> \
                            <li>Scheduled Date and Time: September 2 12:00 - 13:00</li>  \
                            <li>Conflict Type: Has the same Equipment LSNDS</li>  \
                            ",True)
    
    with top_cols[1]:
        unscheduled = st.expander("⚠️ Three tests have not been scheduled on any Enviroment", expanded=True)

        with unscheduled:
            with st.container(border=True):
                st.warning("Adaptability Simulation 1 is not scheduled on any Site/Env", icon="⚠️")
                st.markdown("<li>Scheduled Date and Time: September 2 12:00 - 13:00</li>  \
                            <li>Test Equipment: LSNDS_PhysicsModel1</li> \
                            <li>Conflict Type: No Environment</li>  \
                            ",True)
            with st.container(border=True):
                st.warning("Adaptability Simulation 2 is not scheduled on any Site/Env", icon="⚠️")
                st.markdown("<li>Scheduled Date and Time: September 4 12:00 - 13:00</li>  \
                            <li>Test Equipment: LSNDS_PhysicsModel2</li> \
                            <li>Conflict Type: No Environment</li>  \
                            ",True)
            with st.container(border=True):
                st.warning("Electrical Simulation is not scheduled on any Site/Env", icon="⚠️")
                st.markdown("<li>Scheduled Date and Time: September 5 12:00 - 13:00</li>  \
                            <li>Test Equipment: LSNDS_ElectricalModel1</li> \
                            <li>Conflict Type: No Environment</li>  \
                            ",True)

def issuesinfo(height):
    st.markdown("<h6>Issues &nbsp; <i>(scroll to view all)</i> </h6>", True)
    issues_dict = warningdetails()

    with st.container(border=True, height=height):
        for warn in issues_dict["requirement"]:
            st.warning(warn, icon="⚠️")
        for warn in issues_dict["testtime"]:
            st.warning(warn, icon="⚠️")
        for warn in issues_dict["testsite"]:
            st.warning(warn, icon="⚠️")
        for warn in issues_dict["testreq"]:
            st.error(warn, icon="❗")

def warningdetails():

    # not satisfied not verified requirements
    reqs = pd.read_csv("reports/Requirements.csv", index_col=0)

    # scheduling conflicts for time on test subject or test site
    schedule = pd.read_csv("results/Query6_Scheduling copy.csv", index_col=0)

    # test does not have any test site and does not verify requirement
    tests = pd.read_csv("reports/Tests.csv", index_col=0)

    issues_dict = {
        "requirement": [],
        "testtime": [],
        "testsite": [],
        "testreq": []
    }

    # ################ requirement

    for index, row in reqs.iterrows():
        requirement = row['ReqName']
        satisfiedby = row['SatisfiedBy']
        verifiedby = row['VerifiedName']

        if pd.isnull(satisfiedby):
            issues_dict["requirement"].append(f"{requirement} is not satisfied by any System")
        if pd.isnull(verifiedby):
            issues_dict["requirement"].append(f"{requirement} is not verified by any Test/Activity")
    
    # ################ test site and time
    grouped = schedule[schedule["Include"]==True].groupby('Start').filter(lambda x: len(x) > 1)
    time_conflicted_pairs = []
    for time, group in grouped.groupby('Start'):
        vm_names = group['VMName'].tolist()
        pairs = list(combinations(vm_names, 2))
        time_conflicted_pairs.extend(pairs)
    
    grouped = schedule[schedule["Include"]==True].groupby('Start').filter(lambda x: len(x) > 1)
    site_conflicted_pairs = []
    for site, group in grouped.groupby('Site'):
        vm_names = group['VMName'].tolist()
        pairs = list(combinations(vm_names, 2))
        site_conflicted_pairs.extend(pairs)

    for pair in time_conflicted_pairs:
        issues_dict["testtime"].append(f"{pair[0]} and {pair[0]} have potential time overlap")

    for pair in time_conflicted_pairs:
        issues_dict["testsite"].append(f"{pair[0]} and {pair[0]} have test site overlap")

    # ################ test requirement
    for index,row in tests.iterrows():
        verifies = row["VerifiesRequirement"]
        test = row["Test"]
        if pd.isnull(verifies):
            issues_dict["testreq"].append(f"Test {test} does not verify any Requirement")

    return issues_dict