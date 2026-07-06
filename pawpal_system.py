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
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        return self.tasks


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        return [task for pet in self.pets for task in pet.get_tasks()]


@dataclass
class Scheduler:
    owner: Owner

    def get_today_schedule(self) -> List[Task]:
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda task: task.time)

    def filter_tasks(
        self,
        tasks: List[Task],
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> List[Task]:
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
        warnings = []
        time_counts: dict = {}
        for task in tasks:
            time_counts.setdefault(task.time, []).append(task)
        for time, tasks_at_time in time_counts.items():
            if len(tasks_at_time) > 1:
                descriptions = ", ".join(task.description for task in tasks_at_time)
                warnings.append(f"Conflict at {time}: {descriptions}")
        return warnings
