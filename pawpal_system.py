"""Logic layer for PawPal+: Owner, Pet, Task, and Scheduler classes."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    description: str
    time: str
    frequency: str = "once"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return this pet's list of tasks."""
        return self.tasks


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return a flat list of every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.get_tasks()]


@dataclass
class Scheduler:
    owner: Owner

    def get_today_schedule(self) -> List[Task]:
        """Return all tasks for the scheduler's owner."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return the given tasks sorted by their time attribute."""
        return sorted(tasks, key=lambda task: task.time)

    def filter_tasks(
        self,
        tasks: List[Task],
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> List[Task]:
        """Return tasks filtered by pet name and/or completion status."""
        result = tasks
        if pet_name is not None:
            pet_task_ids = {
                id(task)
                for pet in self.owner.pets
                if pet.name == pet_name
                for task in pet.get_tasks()
            }
            result = [task for task in result if id(task) in pet_task_ids]
        if completed is not None:
            result = [task for task in result if task.completed == completed]
        return result

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return warning strings for any tasks that share the same time."""
        warnings = []
        time_counts: dict = {}
        for task in tasks:
            time_counts.setdefault(task.time, []).append(task)
        for time, tasks_at_time in time_counts.items():
            if len(tasks_at_time) > 1:
                descriptions = ", ".join(task.description for task in tasks_at_time)
                warnings.append(f"Conflict at {time}: {descriptions}")
        return warnings
