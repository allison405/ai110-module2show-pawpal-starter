from dataclasses import dataclass, field, replace
from typing import Literal, Optional
from uuid import uuid4


def _fmt_time(minutes: int) -> str:
    """Convert minutes-since-midnight to a readable HH:MM string."""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: Literal["low", "medium", "high"]
    frequency: str = "daily"  # e.g. "daily", "weekly", "as needed"
    completed: bool = False
    notes: str = ""
    start_time: Optional[int] = None  # minutes since midnight, e.g. 480 = 8:00 AM
    id: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self) -> dict:
        """Serialize the task to a dictionary for display or storage."""
        return {
            "id": self.id,
            "title": self.title,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "frequency": self.frequency,
            "completed": self.completed,
            "notes": self.notes,
        }

    def should_recur(self) -> bool:
        """Return True if this task's frequency warrants a new occurrence after completion."""
        return self.frequency in ("daily", "weekly")

    def recur(self) -> "Task":
        """Return a new pending copy of this task for the next occurrence."""
        return replace(self, completed=False, id=str(uuid4()))

    def __repr__(self) -> str:
        """Return a readable one-line summary of the task."""
        status = "done" if self.completed else "pending"
        return f"[{self.priority.upper()}] {self.title} ({self.duration_minutes} min) — {status}"


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove the task with the given ID from this pet's task list."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_tasks_by_priority(self) -> list[Task]:
        """Return all tasks sorted from highest to lowest priority."""
        return sorted(self.tasks, key=lambda t: PRIORITY_ORDER[t.priority])

    def mark_task_complete(self, task_id: str, completed: bool = True) -> None:
        """Mark the task done (True) or not done (False). Recurs only when marking complete."""
        for task in self.tasks:
            if task.id == task_id:
                task.completed = completed
                if completed and task.should_recur():
                    self.tasks.append(task.recur())
                return

    def __repr__(self) -> str:
        """Return a readable summary of the pet and their task count."""
        return f"{self.name} ({self.species}) — {len(self.tasks)} task(s)"


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name from this owner's pet list."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_all_tasks(self) -> list[tuple[str, Task]]:
        """Returns all tasks across all pets as (pet_name, task) pairs."""
        return [(pet.name, task) for pet in self.pets for task in pet.tasks]

    def __repr__(self) -> str:
        """Return a readable summary of the owner and their pet count."""
        return f"Owner: {self.name} — {len(self.pets)} pet(s)"


@dataclass
class Scheduler:
    owner: Owner

    def _pending_tasks(self, pet_name: Optional[str] = None) -> list[tuple[str, Task]]:
        """Collect all pending tasks, optionally filtered to one pet."""
        pets = [p for p in self.owner.pets if p.name == pet_name] if pet_name else self.owner.pets
        return [(pet.name, task) for pet in pets for task in pet.tasks if not task.completed]

    def get_prioritized_tasks(self, pet_name: Optional[str] = None) -> list[tuple[str, Task]]:
        """Returns all pending tasks sorted by priority. Optionally filter by pet name."""
        return sorted(self._pending_tasks(pet_name), key=lambda pair: PRIORITY_ORDER[pair[1].priority])

    def build_weekly_schedule(self) -> dict[str, list[dict]]:
        """Distributes tasks across the week based on frequency and priority."""
        schedule: dict[str, list[dict]] = {day: [] for day in DAYS}

        for pet in self.owner.pets:
            for task in pet.get_tasks_by_priority():
                if task.frequency == "daily":
                    for day in DAYS:
                        schedule[day].append({"pet": pet.name, **task.to_dict()})
                elif task.frequency == "weekly":
                    schedule["Monday"].append({"pet": pet.name, **task.to_dict()})
                # "as needed" tasks are not auto-scheduled

        return schedule

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> list[tuple[str, Task]]:
        """Filter tasks by pet name and/or completion status."""
        results = []
        for pet in self.owner.pets:
            if pet_name and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if completed is not None and task.completed != completed:
                    continue
                results.append((pet.name, task))
        return results

    def sort_by_time(self, pet_name: Optional[str] = None) -> list[tuple[str, Task]]:
        """Return all pending tasks sorted from shortest to longest duration."""
        return sorted(self._pending_tasks(pet_name), key=lambda pair: pair[1].duration_minutes)

    def detect_conflicts(self) -> list[str]:
        """Return warning strings for any tasks whose time windows overlap; never raises."""
        warnings = []
        timed = [
            (pet.name, task)
            for pet in self.owner.pets
            for task in pet.tasks
            if not task.completed and task.start_time is not None
        ]
        for i, (pet_a, task_a) in enumerate(timed):
            a_end = task_a.start_time + task_a.duration_minutes
            for pet_b, task_b in timed[i + 1:]:
                b_end = task_b.start_time + task_b.duration_minutes
                if task_a.start_time < b_end and task_b.start_time < a_end:
                    warnings.append(
                        f"WARNING: '{task_a.title}' ({pet_a}, {_fmt_time(task_a.start_time)}-{_fmt_time(a_end)}) "
                        f"overlaps with '{task_b.title}' ({pet_b}, {_fmt_time(task_b.start_time)}-{_fmt_time(b_end)})"
                    )
        return warnings

    def summarize(self) -> str:
        """Returns a plain-text summary of all pending tasks by pet."""
        lines = [f"Schedule for {self.owner.name}:"]
        for pet in self.owner.pets:
            pending = sorted(
                [task for _, task in self._pending_tasks(pet.name)],
                key=lambda t: PRIORITY_ORDER[t.priority],
            )
            lines.append(f"\n  {pet.name} ({pet.species})")
            if not pending:
                lines.append("    No pending tasks.")
            else:
                for task in pending:
                    lines.append(f"    - {task}")
        return "\n".join(lines)
