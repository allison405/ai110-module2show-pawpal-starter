import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, Owner, Scheduler


# --- Required: Sorting Correctness ---

def test_tasks_returned_in_priority_order():
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(Task(title="Bath",      duration_minutes=45, priority="low"))
    pet.add_task(Task(title="Medication",duration_minutes=5,  priority="high"))
    pet.add_task(Task(title="Brushing",  duration_minutes=15, priority="medium"))
    owner = Owner(name="Jordan", pets=[pet])
    result = Scheduler(owner).get_prioritized_tasks()
    priorities = [task.priority for _, task in result]
    assert priorities == ["high", "medium", "low"]


# --- Required: Recurrence Logic ---

def test_daily_task_creates_new_pending_task_after_complete():
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(Task(title="Walk", duration_minutes=30, priority="high", frequency="daily"))
    original_id = pet.tasks[0].id
    pet.mark_task_complete(original_id)
    pending = [t for t in pet.tasks if not t.completed]
    assert len(pending) == 1
    assert pending[0].title == "Walk"
    assert pending[0].id != original_id


# --- Required: Conflict Detection ---

def test_scheduler_flags_duplicate_start_times():
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(Task(title="Walk",    duration_minutes=30, priority="high", start_time=480))
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high", start_time=480))
    owner = Owner(name="Jordan", pets=[pet])
    warnings = Scheduler(owner).detect_conflicts()
    assert len(warnings) >= 1
    assert "Walk" in warnings[0]
    assert "Feeding" in warnings[0]


# --- Original tests ---

def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(task)
    pet.mark_task_complete(task.id)
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet(name="Mochi", species="cat")
    assert len(pet.tasks) == 0
    pet.add_task(Task(title="Feeding", duration_minutes=5, priority="high"))
    assert len(pet.tasks) == 1
    pet.add_task(Task(title="Litter box", duration_minutes=10, priority="medium"))
    assert len(pet.tasks) == 2


# --- Sorting ---

def test_sort_all_same_priority():
    pet = Pet(name="Mochi", species="cat")
    pet.add_task(Task(title="A", duration_minutes=5,  priority="medium"))
    pet.add_task(Task(title="B", duration_minutes=10, priority="medium"))
    pet.add_task(Task(title="C", duration_minutes=15, priority="medium"))
    owner = Owner(name="Jordan", pets=[pet])
    result = Scheduler(owner).get_prioritized_tasks()
    assert len(result) == 3


def test_sort_excludes_completed():
    pet = Pet(name="Mochi", species="cat")
    pet.add_task(Task(title="Done task", duration_minutes=5, priority="high", frequency="as needed"))
    pet.add_task(Task(title="Pending task", duration_minutes=10, priority="low"))
    pet.mark_task_complete(pet.tasks[0].id)
    owner = Owner(name="Jordan", pets=[pet])
    result = Scheduler(owner).get_prioritized_tasks()
    assert len(result) == 1
    assert result[0][1].title == "Pending task"


def test_sort_by_time_stable_equal_duration():
    pet = Pet(name="Mochi", species="cat")
    pet.add_task(Task(title="A", duration_minutes=10, priority="high"))
    pet.add_task(Task(title="B", duration_minutes=10, priority="low"))
    owner = Owner(name="Jordan", pets=[pet])
    result = Scheduler(owner).sort_by_time()
    assert len(result) == 2
    assert result[0][1].duration_minutes == result[1][1].duration_minutes


def test_sort_empty_pet():
    pet = Pet(name="Ghost", species="cat")
    owner = Owner(name="Jordan", pets=[pet])
    assert Scheduler(owner).get_prioritized_tasks() == []
    assert Scheduler(owner).sort_by_time() == []


# --- Recurring tasks ---

def test_daily_task_recurs_on_complete():
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(Task(title="Walk", duration_minutes=30, priority="high", frequency="daily"))
    pet.mark_task_complete(pet.tasks[0].id)
    assert len(pet.tasks) == 2
    assert pet.tasks[1].completed is False


def test_weekly_task_recurs_on_complete():
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(Task(title="Bath", duration_minutes=45, priority="low", frequency="weekly"))
    pet.mark_task_complete(pet.tasks[0].id)
    assert len(pet.tasks) == 2
    assert pet.tasks[1].completed is False


def test_as_needed_task_does_not_recur():
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(Task(title="Vet visit", duration_minutes=60, priority="high", frequency="as needed"))
    pet.mark_task_complete(pet.tasks[0].id)
    assert len(pet.tasks) == 1


def test_completing_already_completed_task_does_not_double_recur():
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(Task(title="Walk", duration_minutes=30, priority="high", frequency="daily"))
    pet.mark_task_complete(pet.tasks[0].id)  # completes + recurs → 2 tasks
    pet.mark_task_complete(pet.tasks[0].id)  # calling again on already-done task
    assert len(pet.tasks) == 3  # one extra recurrence, not two


def test_recurred_task_copies_fields():
    original = Task(title="Feeding", duration_minutes=5, priority="high", frequency="daily", notes="wet food")
    recurred = original.recur()
    assert recurred.title == original.title
    assert recurred.duration_minutes == original.duration_minutes
    assert recurred.priority == original.priority
    assert recurred.frequency == original.frequency
    assert recurred.notes == original.notes
    assert recurred.completed is False


def test_recurred_task_has_new_id():
    original = Task(title="Feeding", duration_minutes=5, priority="high", frequency="daily")
    recurred = original.recur()
    assert recurred.id != original.id


# --- Conflict detection ---

def test_conflict_identical_start_time():
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(Task(title="Walk",     duration_minutes=30, priority="high", start_time=480))
    pet.add_task(Task(title="Feeding",  duration_minutes=10, priority="high", start_time=480))
    owner = Owner(name="Jordan", pets=[pet])
    warnings = Scheduler(owner).detect_conflicts()
    assert len(warnings) == 1


def test_conflict_partial_overlap():
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(Task(title="Walk",    duration_minutes=30, priority="high", start_time=480))
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high", start_time=500))
    owner = Owner(name="Jordan", pets=[pet])
    warnings = Scheduler(owner).detect_conflicts()
    assert len(warnings) == 1


def test_no_conflict_back_to_back():
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(Task(title="Walk",    duration_minutes=30, priority="high", start_time=480))
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high", start_time=510))
    owner = Owner(name="Jordan", pets=[pet])
    warnings = Scheduler(owner).detect_conflicts()
    assert warnings == []


def test_no_conflict_tasks_without_start_time():
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(Task(title="Walk",    duration_minutes=30, priority="high"))
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))
    owner = Owner(name="Jordan", pets=[pet])
    warnings = Scheduler(owner).detect_conflicts()
    assert warnings == []


def test_completed_tasks_excluded_from_conflict_check():
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(Task(title="Walk",    duration_minutes=30, priority="high", frequency="as needed", start_time=480))
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high", start_time=480))
    pet.mark_task_complete(pet.tasks[0].id)
    owner = Owner(name="Jordan", pets=[pet])
    warnings = Scheduler(owner).detect_conflicts()
    assert warnings == []


# --- Multi-pet / Owner ---

def test_owner_with_no_pets():
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner)
    assert scheduler.get_prioritized_tasks() == []
    assert scheduler.build_weekly_schedule() == {d: [] for d in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]}
    assert "Jordan" in scheduler.summarize()


def test_cross_pet_conflict_detected():
    pet_a = Pet(name="Mochi",   species="cat")
    pet_b = Pet(name="Biscuit", species="dog")
    pet_a.add_task(Task(title="Feeding", duration_minutes=20, priority="high", start_time=480))
    pet_b.add_task(Task(title="Walk",    duration_minutes=30, priority="high", start_time=480))
    owner = Owner(name="Jordan", pets=[pet_a, pet_b])
    warnings = Scheduler(owner).detect_conflicts()
    assert len(warnings) == 1


def test_filter_nonexistent_pet_returns_empty():
    pet = Pet(name="Mochi", species="cat")
    pet.add_task(Task(title="Feeding", duration_minutes=5, priority="high"))
    owner = Owner(name="Jordan", pets=[pet])
    result = Scheduler(owner).filter_tasks(pet_name="Ghost")
    assert result == []
