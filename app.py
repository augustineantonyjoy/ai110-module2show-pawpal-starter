import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(owner_name)
owner = st.session_state["owner"]

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "pet" not in st.session_state:
    st.session_state["pet"] = Pet(pet_name, species)
    owner.add_pet(st.session_state["pet"])
pet = st.session_state["pet"]

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    task_time = st.text_input("Time", value="08:00")
with col3:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col4:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    pet.add_task(Task(task_title, task_time))

if pet.get_tasks():
    st.write("Current tasks:")
    for i, task in enumerate(pet.get_tasks()):
        row1, row2, row3, row4 = st.columns([3, 1, 1, 1])
        row1.write(task.description)
        row2.write(task.time)
        row3.write(task.frequency)
        if task.completed:
            row4.write("✅ completed")
        else:
            if row4.checkbox("Mark complete", key=f"complete_task_{i}"):
                pet.complete_task(task)
                st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time(scheduler.get_today_schedule())
    conflicts = scheduler.detect_conflicts(sorted_tasks)
    if conflicts:
        for conflict in conflicts:
            st.warning(conflict)
    else:
        st.success("No scheduling conflicts detected.")

    if sorted_tasks:
        st.success(f"Schedule generated with {len(sorted_tasks)} task(s).")
        st.table(
            [
                {
                    "description": task.description,
                    "time": task.time,
                    "frequency": task.frequency,
                    "completed": task.completed,
                }
                for task in sorted_tasks
            ]
        )
    else:
        st.info("No tasks to schedule yet. Add one above.")
