import streamlit as st


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

def issuesinfo():
    st.markdown("<h6>Issues</h6>", True)
    with st.container(border=True, height=350):
        st.warning('Four tests have overlapped scheduling (find more info on Issues tab)', icon="⚠️")