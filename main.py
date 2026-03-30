from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Jordan")

mochi = Pet(name="Mochi", species="cat")
biscuit = Pet(name="Biscuit", species="dog")

# --- Tasks for Mochi (cat) ---
mochi.add_task(Task(title="Feeding",        duration_minutes=5,  priority="high",   frequency="daily"))
mochi.add_task(Task(title="Litter box",     duration_minutes=10, priority="medium", frequency="daily"))
mochi.add_task(Task(title="Brushing",       duration_minutes=15, priority="low",    frequency="weekly"))

# --- Tasks for Biscuit (dog) ---
biscuit.add_task(Task(title="Morning walk", duration_minutes=30, priority="high",   frequency="daily"))
biscuit.add_task(Task(title="Medication",   duration_minutes=5,  priority="high",   frequency="daily"))
biscuit.add_task(Task(title="Bath time",    duration_minutes=45, priority="low",    frequency="weekly",
                      notes="Use oatmeal shampoo"))

owner.add_pet(mochi)
owner.add_pet(biscuit)

# --- Scheduler ---
scheduler = Scheduler(owner=owner)

# --- Print Today's Schedule ---
print("=" * 40)
print("       TODAY'S SCHEDULE")
print("=" * 40)

today_tasks = scheduler.get_prioritized_tasks()

if not today_tasks:
    print("No pending tasks today!")
else:
    for pet_name, task in today_tasks:
        print(f"  [{task.priority.upper():6}] {task.title:<20} {task.duration_minutes} min  —  {pet_name}")

print("=" * 40)
print(f"Total tasks: {len(today_tasks)}")
print()

# --- Full summary ---
print(scheduler.summarize())
