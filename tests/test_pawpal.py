import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(task)

    pet.mark_complete(task.id)

    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet(name="Mochi", species="cat")
    assert len(pet.tasks) == 0

    pet.add_task(Task(title="Feeding", duration_minutes=5, priority="high"))
    assert len(pet.tasks) == 1

    pet.add_task(Task(title="Litter box", duration_minutes=10, priority="medium"))
    assert len(pet.tasks) == 2
