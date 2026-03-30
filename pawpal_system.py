from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", or "high"
    day_of_week: str = ""
    notes: str = ""

    def to_dict(self) -> dict:
        pass

    def __repr__(self) -> str:
        pass


@dataclass
class TaskList:
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, title: str) -> None:
        pass

    def get_by_priority(self) -> list[Task]:
        pass

    def get_by_day(self, day: str) -> list[Task]:
        pass


@dataclass
class WeeklySchedule:
    schedule: dict[str, list[Task]] = field(default_factory=dict)

    def assign_task(self, task: Task, day: str) -> None:
        pass

    def get_day(self, day: str) -> list[Task]:
        pass

    def display(self) -> dict:
        pass


@dataclass
class Pet:
    name: str
    species: str
    task_list: TaskList = field(default_factory=TaskList)


@dataclass
class Owner:
    name: str
    pet: Optional[Pet] = None
