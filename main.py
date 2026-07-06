"""Manual CLI check for the PawPal+ backend logic."""

from tabulate import tabulate

from pawpal_system import Owner, Pet, Task, Scheduler

STATUS_EMOJI = {True: "✅", False: "⏳"}
PRIORITY_EMOJI = {"high": "🔴", "medium": "🟡", "low": "🟢"}


def main() -> None:
    owner = Owner("Alice")

    dog = Pet("Rex", "Dog")
    cat = Pet("Whiskers", "Cat")

    dog.add_task(Task("Morning walk", "08:00", priority="high"))
    dog.add_task(Task("Give medication", "09:00", frequency="daily", priority="low"))
    cat.add_task(Task("Feed breakfast", "08:00"))
    cat.add_task(Task("Clean litter box", "18:30", frequency="daily"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)

    pet_by_task = {
        id(task): pet for pet in owner.pets for task in pet.get_tasks()
    }

    schedule = scheduler.sort_by_time(scheduler.get_today_schedule())

    print("=== Today's Schedule ===")
    rows = [
        [
            task.time,
            pet_by_task[id(task)].name,
            task.description,
            task.frequency,
            f"{STATUS_EMOJI[task.completed]} {'Done' if task.completed else 'Pending'}",
        ]
        for task in schedule
    ]
    print(tabulate(rows, headers=["Time", "Pet", "Description", "Frequency", "Status"], tablefmt="simple"))

    conflicts = scheduler.detect_conflicts(schedule)
    if conflicts:
        print("\n=== Conflicts ===")
        for warning in conflicts:
            print(warning)

    rex_tasks = scheduler.filter_tasks(schedule, pet_name="Rex")
    print("\n=== Rex's Tasks Only ===")
    rows = [
        [
            task.time,
            "Rex",
            task.description,
            task.frequency,
            f"{STATUS_EMOJI[task.completed]} {'Done' if task.completed else 'Pending'}",
        ]
        for task in rex_tasks
    ]
    print(tabulate(rows, headers=["Time", "Pet", "Description", "Frequency", "Status"], tablefmt="simple"))

    daily_task = next(task for task in dog.get_tasks() if task.description == "Give medication")
    dog.complete_task(daily_task)

    updated_schedule = scheduler.sort_by_time(scheduler.get_today_schedule())
    updated_pet_by_task = {
        id(task): pet for pet in owner.pets for task in pet.get_tasks()
    }

    print("\n=== Schedule After Completing Daily Task ===")
    rows = [
        [
            task.time,
            updated_pet_by_task[id(task)].name,
            task.description,
            task.frequency,
            f"{STATUS_EMOJI[task.completed]} {'Done' if task.completed else 'Pending'}",
            task.due_date,
        ]
        for task in updated_schedule
    ]
    print(tabulate(rows, headers=["Time", "Pet", "Description", "Frequency", "Status", "Due"], tablefmt="simple"))

    priority_schedule = scheduler.sort_by_priority_then_time(scheduler.get_today_schedule())

    print("\n=== Schedule by Priority ===")
    rows = [
        [
            f"{PRIORITY_EMOJI[task.priority]} {task.priority}",
            task.time,
            task.description,
        ]
        for task in priority_schedule
    ]
    print(tabulate(rows, headers=["Priority", "Time", "Description"], tablefmt="simple"))


if __name__ == "__main__":
    main()
