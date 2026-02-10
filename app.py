import streamlit as st
from sheets import get_sheet

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(page_title="Skylark Drone Ops", layout="wide")
st.title("Skylark Drone Operations Coordinator")
st.caption("Internal operations dashboard for pilot, drone, and mission coordination")

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------
pilot_df, pilot_ws = get_sheet("pilot_roster")
mission_df, _ = get_sheet("missions")
drone_df, drone_ws = get_sheet("drone_fleet")

# =====================================================
# SIDEBAR — OPERATIONS PANEL
# =====================================================
st.sidebar.header("Operations Panel")
st.sidebar.caption("Quick actions for live coordination")

# ---------- Pilot Status ----------
with st.sidebar.container():
    st.sidebar.subheader("Pilot Availability")

    sel_pilot = st.sidebar.selectbox(
        "Select pilot",
        pilot_df["name"].tolist()
    )

    new_pilot_status = st.sidebar.selectbox(
        "Set status",
        ["Available", "On Leave", "Unavailable"]
    )

    if st.sidebar.button("Update Pilot Status"):
        row = pilot_df[pilot_df["name"] == sel_pilot].index[0] + 2
        pilot_ws.update(f"F{row}", [[new_pilot_status]])
        st.sidebar.success("Pilot status updated")

# ---------- Drone Status ----------
with st.sidebar.container():
    st.sidebar.subheader("Drone Status")

    sel_drone = st.sidebar.selectbox(
        "Select drone",
        drone_df["drone_id"].tolist()
    )

    new_drone_status = st.sidebar.selectbox(
        "Set status",
        ["Available", "Deployed", "In Maintenance"]
    )

    if st.sidebar.button("Update Drone Status"):
        row = drone_df[drone_df["drone_id"] == sel_drone].index[0] + 2
        drone_ws.update(f"D{row}", [[new_drone_status]])
        st.sidebar.success("Drone status updated")

# ---------- Mission Selection ----------
st.sidebar.divider()
st.sidebar.subheader("Mission Context")

sel_project = st.sidebar.selectbox(
    "Active mission",
    mission_df["project_id"].tolist()
)

# =====================================================
# MAIN CONTENT — LIVE DATA
# =====================================================
st.subheader("Pilot Roster (Live)")
st.dataframe(pilot_df, use_container_width=True)

st.subheader("Missions (Live)")
st.dataframe(mission_df, use_container_width=True)

st.subheader("Drone Inventory (Live)")
st.dataframe(drone_df, use_container_width=True)

maintenance = drone_df[
    drone_df["status"].str.contains("Maintenance", case=False, na=False)
]
if not maintenance.empty:
    st.warning("Some drones are currently under maintenance")

# =====================================================
# MISSION ASSIGNMENT FLOW
# =====================================================
st.divider()
st.subheader("Mission Assignment")

mission = mission_df[
    mission_df["project_id"] == sel_project
].iloc[0]

st.markdown(
    f"""
    **Mission Overview**

    - Project ID: {mission['project_id']}
    - Location: {mission['location']}
    - Required Skill: {mission['required_skills']}
    - Required Certification: {mission['required_certs']}
    - Priority: {mission['priority']}
    """
)

# ---------- Drone Selection ----------
st.markdown("### Step 1: Select Drone")

selected_drone = st.selectbox(
    "Choose a drone for this mission",
    drone_df["drone_id"].tolist()
)

drone_row = drone_df[
    drone_df["drone_id"] == selected_drone
].iloc[0]

if drone_row["location"] != mission["location"]:
    st.warning(
        f"Drone location mismatch: Drone is in {drone_row['location']}, "
        f"mission is in {mission['location']}."
    )

# =====================================================
# PILOT EVALUATION
# =====================================================
st.markdown("### Step 2: Pilot Evaluation")

required_skill = mission["required_skills"].strip().lower()
required_cert = mission["required_certs"].strip().lower()

eligible = []
rejected = []

for _, p in pilot_df.iterrows():
    skills = [s.strip().lower() for s in str(p["skills"]).split(",")]
    certs = [c.strip().lower() for c in str(p["certifications"]).split(",")]

    if p["location"] != mission["location"]:
        rejected.append((p["name"], "Location mismatch"))
        continue
    if p["status"] != "Available":
        rejected.append((p["name"], f"Status: {p['status']}"))
        continue
    if required_skill not in skills:
        rejected.append((p["name"], "Missing required skill"))
        continue
    if required_cert not in certs:
        rejected.append((p["name"], "Missing required certification"))
        continue

    eligible.append(p)

# =====================================================
# FINAL DECISION
# =====================================================
st.divider()
st.subheader("Assignment Decision")

if eligible:
    chosen = eligible[0]

    st.success(f"Recommended Pilot: {chosen['name']}")

    if str(chosen["current_assignment"]).strip():
        st.warning(
            f"This pilot is already assigned to {chosen['current_assignment']}. "
            "Please confirm that project dates do not overlap."
        )

    if st.button("Confirm Assignment"):
        row = pilot_df[pilot_df["name"] == chosen["name"]].index[0] + 2
        pilot_ws.update(f"F{row}", [["Assigned"]])
        pilot_ws.update(f"G{row}", [[mission["project_id"]]])
        st.success("Pilot successfully assigned to mission")
else:
    st.error("No suitable pilot available for this mission")

with st.expander("View rejected pilots and reasons"):
    for name, reason in rejected:
        st.write(f"{name}: {reason}")
