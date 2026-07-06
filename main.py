"""Manual CLI check for the PawPal+ backend logic."""

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner("Alice")

    dog = Pet("Rex", "Dog")
    cat = Pet("Whiskers", "Cat")

    dog.add_task(Task("Morning walk", "08:00"))
    dog.add_task(Task("Give medication", "09:00", frequency="daily"))
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
    for task in schedule:
        pet = pet_by_task[id(task)]
        status = "Done" if task.completed else "Pending"
        print(
            f"[{task.time}] {pet.name} - {task.description} "
            f"(frequency: {task.frequency}, status: {status})"
        )

    conflicts = scheduler.detect_conflicts(schedule)
    if conflicts:
        print("\n=== Conflicts ===")
        for warning in conflicts:
            print(warning)


if __name__ == "__main__":
    main()
