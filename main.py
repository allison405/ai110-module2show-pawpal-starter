from pawpal_system import Task, Pet, Owner, Scheduler

def print_tasks(label: str, tasks: list) -> None:
    print(f"\n{label}")
    print("-" * 40)
    if not tasks:
        print("  (none)")
    else:
        for pet_name, task in tasks:
            status = "done" if task.completed else "pending"
            print(f"  [{task.priority.upper():6}] {task.title:<22} {task.duration_minutes:>3} min  |  {pet_name}  |  {status}")

# --- Setup ---
owner = Owner(name="Jordan")

mochi = Pet(name="Mochi", species="cat")
biscuit = Pet(name="Biscuit", species="dog")

# Tasks added intentionally out of order (low before high, long before short)
# start_time = minutes since midnight  (e.g. 480 = 8:00 AM, 500 = 8:20 AM)
mochi.add_task(Task(title="Brushing",       duration_minutes=15, priority="low",    frequency="weekly", start_time=480))
mochi.add_task(Task(title="Litter box",     duration_minutes=10, priority="medium", frequency="daily",  start_time=490))  # overlaps Brushing (480-495)
mochi.add_task(Task(title="Feeding",        duration_minutes=5,  priority="high",   frequency="daily",  start_time=510))

biscuit.add_task(Task(title="Bath time",    duration_minutes=45, priority="low",    frequency="weekly", start_time=600))
biscuit.add_task(Task(title="Morning walk", duration_minutes=30, priority="high",   frequency="daily",  start_time=480))
biscuit.add_task(Task(title="Medication",   duration_minutes=5,  priority="high",   frequency="daily",  start_time=500))  # overlaps Morning walk (480-510)

owner.add_pet(mochi)
owner.add_pet(biscuit)

# Mark one task complete to test filtering
biscuit.mark_task_complete(biscuit.tasks[1].id)  # Morning walk -> done

scheduler = Scheduler(owner=owner)

# --- Sort by priority ---
print_tasks("SORTED BY PRIORITY (all pets)", scheduler.get_prioritized_tasks())

# --- Sort by duration ---
print_tasks("SORTED BY TIME / DURATION (all pets)", scheduler.sort_by_time())

# --- Filter: pending only ---
print_tasks("FILTER — pending tasks only", scheduler.filter_tasks(completed=False))

# --- Filter: completed only ---
print_tasks("FILTER — completed tasks only", scheduler.filter_tasks(completed=True))

# --- Filter: one pet ---
print_tasks("FILTER — Mochi's tasks only", scheduler.filter_tasks(pet_name="Mochi"))

# --- Filter: one pet + pending ---
print_tasks("FILTER — Biscuit's pending tasks only", scheduler.filter_tasks(pet_name="Biscuit", completed=False))

print()

# --- Conflict detection ---
print("\nCONFLICT DETECTION")
print("-" * 40)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for w in conflicts:
        print(" ", w)
else:
    print("  No conflicts found.")

print()
