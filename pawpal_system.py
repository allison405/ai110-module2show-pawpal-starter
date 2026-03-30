from dataclasses import dataclass, field
from typing import Literal, Optional
from uuid import uuid4

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

    def mark_complete(self, task_id: str) -> None:
        """Mark the task with the given ID as completed."""
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
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

    def get_prioritized_tasks(self, pet_name: Optional[str] = None) -> list[tuple[str, Task]]:
        """Returns all pending tasks sorted by priority. Optionally filter by pet name."""
        if pet_name:
            pets = [p for p in self.owner.pets if p.name == pet_name]
        else:
            pets = self.owner.pets

        all_tasks = [(pet.name, task) for pet in pets for task in pet.tasks if not task.completed]
        return sorted(all_tasks, key=lambda pair: PRIORITY_ORDER[pair[1].priority])

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

    def summarize(self) -> str:
        """Returns a plain-text summary of all pending tasks by pet."""
        lines = [f"Schedule for {self.owner.name}:"]
        for pet in self.owner.pets:
            pending = [t for t in pet.tasks if not t.completed]
            lines.append(f"\n  {pet.name} ({pet.species})")
            if not pending:
                lines.append("    No pending tasks.")
            else:
                for task in sorted(pending, key=lambda t: PRIORITY_ORDER[t.priority]):
                    lines.append(f"    - {task}")
        return "\n".join(lines)
