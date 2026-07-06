from pawpal_system import Task, Pet


def test_task_completion():
    task = Task("Feed breakfast", "08:00")
    task.mark_complete()
    assert task.completed is True


def test_task_addition():
    pet = Pet("Rex", "Dog")
    initial_count = len(pet.get_tasks())
    pet.add_task(Task("Morning walk", "08:00"))
    assert len(pet.get_tasks()) == initial_count + 1
