import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Session state init ---
if "owner" not in st.session_state:
    st.session_state.owner = None

# --- Owner setup ---
st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
if st.button("Set owner"):
    st.session_state.owner = Owner(name=owner_name)
    st.success(f"Owner set to {owner_name}.")

st.divider()

if st.session_state.owner is None:
    st.info("Set an owner name above to get started.")
    st.stop()

owner: Owner = st.session_state.owner
scheduler = Scheduler(owner=owner)

# --- Add a pet ---
st.subheader("Pets")
col1, col2 = st.columns(2)
with col1:
    new_pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    new_species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if any(p.name == new_pet_name for p in owner.pets):
        st.warning(f"A pet named '{new_pet_name}' already exists.")
    else:
        owner.add_pet(Pet(name=new_pet_name, species=new_species))
        st.success(f"Added {new_pet_name} ({new_species}).")

st.divider()

# --- Task lists ---
st.subheader("Task Lists")

if not owner.pets:
    st.info("Add a pet above to get started.")
else:
    # Add a task form
    with st.expander("Add a task"):
        pet_names = [p.name for p in owner.pets]
        selected_pet_name = st.selectbox("Assign to pet", pet_names)
        col1, col2, col3 = st.columns(3)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk")
        with col2:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with col3:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"])
        notes = st.text_input("Notes (optional)", value="")

        if st.button("Add task"):
            task = Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
                frequency=frequency,
                notes=notes,
            )
            pet = next(p for p in owner.pets if p.name == selected_pet_name)
            pet.add_task(task)
            st.success(f"Added '{task_title}' to {selected_pet_name}.")

    # Per-pet task lists with checkboxes
    PRIORITY_BADGE = {"high": "🔴", "medium": "🟡", "low": "🟢"}

    for pet in owner.pets:
        st.markdown(f"### {pet.name} ({pet.species})")
        if not pet.tasks:
            st.caption("No tasks yet.")
        else:
            for task in pet.get_tasks_by_priority():
                col_check, col_label, col_meta = st.columns([1, 4, 3])
                with col_check:
                    checked = st.checkbox(
                        label="done",
                        value=task.completed,
                        key=task.id,
                        label_visibility="collapsed",
                    )
                    if checked != task.completed:
                        task.completed = checked
                        st.rerun()
                with col_label:
                    badge = PRIORITY_BADGE[task.priority]
                    label = f"~~{task.title}~~" if task.completed else f"{badge} {task.title}"
                    st.markdown(label)
                with col_meta:
                    st.caption(f"{task.duration_minutes} min · {task.frequency}")

st.divider()

# --- Schedule & insights ---
st.subheader("Schedule & Insights")

if not owner.pets:
    st.info("Add a pet and some tasks first.")
else:
    # Conflict warnings — shown always, not just on button press
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for w in conflicts:
            st.warning(w)
    else:
        st.success("No scheduling conflicts detected.")

    # Sorted task view
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Sort by priority"):
            st.session_state["schedule_view"] = "priority"
    with col_b:
        if st.button("Sort by duration"):
            st.session_state["schedule_view"] = "duration"

    view = st.session_state.get("schedule_view")
    if view == "priority":
        rows = scheduler.get_prioritized_tasks()
        if rows:
            st.table([
                {"Pet": pet_name, "Task": t.title, "Priority": t.priority, "Duration (min)": t.duration_minutes}
                for pet_name, t in rows
            ])
        else:
            st.info("No pending tasks.")
    elif view == "duration":
        rows = scheduler.sort_by_time()
        if rows:
            st.table([
                {"Pet": pet_name, "Task": t.title, "Duration (min)": t.duration_minutes, "Priority": t.priority}
                for pet_name, t in rows
            ])
        else:
            st.info("No pending tasks.")

    # Weekly schedule
    if st.button("Generate weekly schedule"):
        weekly = scheduler.build_weekly_schedule()
        has_any = any(tasks for tasks in weekly.values())
        if not has_any:
            st.info("No tasks scheduled. Add daily or weekly tasks first.")
        else:
            for day, tasks in weekly.items():
                if tasks:
                    with st.expander(day):
                        st.table([
                            {"Pet": t["pet"], "Task": t["title"], "Priority": t["priority"], "Duration (min)": t["duration_minutes"]}
                            for t in tasks
                        ])
