# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
=== Today's Schedule ===
[08:00] Rex - Morning walk (frequency: once, status: Pending)
[08:00] Whiskers - Feed breakfast (frequency: once, status: Pending)
[09:00] Rex - Give medication (frequency: daily, status: Pending)
[18:30] Whiskers - Clean litter box (frequency: daily, status: Pending)

=== Conflicts ===
Conflict at 08:00: Morning walk, Feed breakfast
```

## 🧪 Testing PawPal+

The test suite covers task completion, task addition, chronological sorting of the daily schedule, daily/weekly recurrence when a task is completed, and detection of time conflicts between tasks.

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
tests/test_pawpal.py::test_task_completion PASSED                        [ 20%]
tests/test_pawpal.py::test_task_addition PASSED                          [ 40%]
tests/test_pawpal.py::test_sorting_correctness PASSED                    [ 60%]
tests/test_pawpal.py::test_recurrence_logic PASSED                       [ 80%]
tests/test_pawpal.py::test_conflict_detection PASSED                     [100%]

5 passed in 0.01s
```

**Confidence Level:** ⭐⭐⭐⭐ (4/5) — all core scheduling behaviors pass reliably, though the suite is still small and doesn't yet cover edge cases like weekly recurrence or filtering.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks chronologically by their time (HH:MM) attribute |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet_name and/or completed status, either independently or combined |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags tasks that share the exact same time, returning warning strings instead of raising an error |
| Recurring tasks | `Task.next_occurrence()` / `Pet.complete_task()` | On completing a "daily" or "weekly" task, automatically creates the next occurrence with due_date advanced by 1 day or 1 week |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
