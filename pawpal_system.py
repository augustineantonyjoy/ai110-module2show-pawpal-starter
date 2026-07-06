"""Logic layer for PawPal+: Owner, Pet, Task, and Scheduler classes."""

import json
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import List, Optional


@dataclass
class Task:
    description: str
    time: str
    frequency: str = "once"
    completed: bool = False
    due_date: date = field(default_factory=date.today)
    priority: str = "medium"

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """Return the next recurring Task instance, or None if this task doesn't recur."""
        if self.frequency == "once":
            return None
        if self.frequency == "daily":
            delta = timedelta(days=1)
        elif self.frequency == "weekly":
            delta = timedelta(weeks=1)
        else:
            return None
        return Task(
            description=self.description,
            time=self.time,
            frequency=self.frequency,
            completed=False,
            due_date=self.due_date + delta,
        )


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

    def complete_task(self, task: Task) -> None:
        """Mark a task complete and schedule its next occurrence, if any."""
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is not None:
            self.add_task(next_task)


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

    def save_to_json(self, filepath: str = "data.json") -> None:
        """Serialize this owner, its pets, and their tasks to a JSON file."""
        data = {
            "name": self.name,
            "pets": [
                {
                    "name": pet.name,
                    "species": pet.species,
                    "tasks": [
                        {
                            "description": task.description,
                            "time": task.time,
                            "frequency": task.frequency,
                            "completed": task.completed,
                            "due_date": task.due_date.isoformat(),
                            "priority": task.priority,
                        }
                        for task in pet.get_tasks()
                    ],
                }
                for pet in self.pets
            ],
        }
        with open(filepath, "w") as f:
            json.dump(data, f)

    @classmethod
    def load_from_json(cls, filepath: str = "data.json") -> "Owner":
        """Load an Owner and its pets/tasks from a JSON file, or return a new empty Owner if missing."""
        if not Path(filepath).exists():
            return cls(name="Owner")
        with open(filepath) as f:
            data = json.load(f)
        pets = [
            Pet(
                name=pet_data["name"],
                species=pet_data["species"],
                tasks=[
                    Task(
                        description=task_data["description"],
                        time=task_data["time"],
                        frequency=task_data["frequency"],
                        completed=task_data["completed"],
                        due_date=date.fromisoformat(task_data["due_date"]),
                        priority=task_data["priority"],
                    )
                    for task_data in pet_data["tasks"]
                ],
            )
            for pet_data in data["pets"]
        ]
        return cls(name=data["name"], pets=pets)


@dataclass
class Scheduler:
    owner: Owner

    def get_today_schedule(self) -> List[Task]:
        """Return all tasks for the scheduler's owner."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return the given tasks sorted by their time attribute."""
        return sorted(tasks, key=lambda task: task.time)

    def sort_by_priority_then_time(self, tasks: List[Task]) -> List[Task]:
        """Return the given tasks sorted by priority (high to low), then by time."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda task: (priority_order[task.priority], task.time))

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
