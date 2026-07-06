from datetime import date, timedelta

from pawpal_system import Task, Pet, Owner, Scheduler


def test_task_completion():
    task = Task("Feed breakfast", "08:00")
    task.mark_complete()
    assert task.completed is True


def test_task_addition():
    pet = Pet("Rex", "Dog")
    initial_count = len(pet.get_tasks())
    pet.add_task(Task("Morning walk", "08:00"))
    assert len(pet.get_tasks()) == initial_count + 1


def test_sorting_correctness():
    pet = Pet("Rex", "Dog")
    pet.add_task(Task("Task A", "10:00"))
    pet.add_task(Task("Task B", "08:00"))
    pet.add_task(Task("Task C", "09:00"))
    owner = Owner("Alice", pets=[pet])
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time(scheduler.get_today_schedule())

    assert [task.time for task in sorted_tasks] == ["08:00", "09:00", "10:00"]


def test_recurrence_logic():
    due_date = date(2026, 7, 5)
    task = Task("Give medicine", "09:00", frequency="daily", due_date=due_date)
    pet = Pet("Rex", "Dog", tasks=[task])

    pet.complete_task(task)

    assert task.completed is True
    assert len(pet.get_tasks()) == 2
    new_task = pet.get_tasks()[-1]
    assert new_task.due_date == due_date + timedelta(days=1)


def test_priority_sorting():
    pet = Pet("Rex", "Dog")
    pet.add_task(Task("Task A", "09:00", priority="low"))
    pet.add_task(Task("Task B", "08:00", priority="high"))
    pet.add_task(Task("Task C", "10:00", priority="medium"))
    owner = Owner("Alice", pets=[pet])
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_priority_then_time(scheduler.get_today_schedule())

    assert [task.description for task in sorted_tasks] == ["Task B", "Task C", "Task A"]


def test_conflict_detection():
    pet = Pet("Rex", "Dog")
    pet.add_task(Task("Feed breakfast", "08:00"))
    pet.add_task(Task("Give medicine", "08:00"))
    owner = Owner("Alice", pets=[pet])
    scheduler = Scheduler(owner)

    conflicts = scheduler.detect_conflicts(scheduler.get_today_schedule())

    assert len(conflicts) > 0
    assert any("08:00" in warning for warning in conflicts)
