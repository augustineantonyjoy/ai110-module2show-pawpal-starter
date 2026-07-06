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

## ✨ Features

- **Chronological sorting** — `Scheduler.sort_by_time()` orders a pet owner's tasks by time (HH:MM) so the daily schedule reads top to bottom.
- **Filtering by pet/status** — `Scheduler.filter_tasks()` narrows the task list by pet name and/or completion status, independently or combined.
- **Time-conflict warnings** — `Scheduler.detect_conflicts()` flags any tasks scheduled at the same time and returns human-readable warning strings instead of raising errors.
- **Daily/weekly recurrence** — `Task.next_occurrence()` and `Pet.complete_task()` automatically generate the next occurrence of a "daily" or "weekly" task (with `due_date` advanced by one day or one week) as soon as the current one is marked complete.
- **Priority-based scheduling** — `Scheduler.sort_by_priority_then_time()` orders tasks by priority (high → medium → low), breaking ties within a priority group by time.
- **Data persistence** — `Owner.save_to_json()` and `Owner.load_from_json()` save and restore an owner's pets and tasks to/from a JSON file, so data survives an app restart.
- **Polished output formatting** — emoji status (✅/⏳) and priority (🔴/🟡/🟢) indicators throughout, with `main.py` rendering its schedule sections as aligned tables via `tabulate`.
- **Next available slot finder** — `Scheduler.find_next_available_slot()` takes a desired duration and scans a pet's existing tasks (using each task's `duration_minutes`) to return the first open `"HH:MM"` gap between `day_start` and `day_end`, or `None` if the day is fully booked.

## 🔍 Next Available Slot

Given a duration and a pet's existing tasks, `Scheduler.find_next_available_slot(tasks, duration_minutes, day_start="06:00", day_end="22:00")` treats each task as a busy interval (`time` to `time + duration_minutes`), sorts them, and walks forward from `day_start` looking for the first gap big enough to fit the requested duration — returning `None` if no such gap exists before `day_end`. This is what finally makes the "Duration (minutes)" input in `app.py`'s Add Task form meaningful — it's now stored on the `Task` (`duration_minutes`) and persisted through `save_to_json`/`load_from_json`, instead of being collected and discarded.

Sample CLI output from `main.py`:

```
=== Next Available 45-Minute Slot ===
06:00
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks chronologically by their time (HH:MM) attribute |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet_name and/or completed status, either independently or combined |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags tasks that share the exact same time, returning warning strings instead of raising an error |
| Recurring tasks | `Task.next_occurrence()` / `Pet.complete_task()` | On completing a "daily" or "weekly" task, automatically creates the next occurrence with due_date advanced by 1 day or 1 week |
| Priority scheduling | `Scheduler.sort_by_priority_then_time()` | Sorts tasks by priority (high → medium → low), then by time within each priority group |

### Priority Scheduling

Running `python main.py` also prints the schedule ordered by priority:

```
=== Schedule by Priority ===
[high] 08:00 - Morning walk
[medium] 08:00 - Feed breakfast
[medium] 09:00 - Give medication
[medium] 18:30 - Clean litter box
[low] 09:00 - Give medication
```

## 💾 Data Persistence

Data is saved to `data.json` in the project root every time a pet, task, or task completion is added/changed.

On app startup, `Owner.load_from_json()` reconstructs the owner, its pets, and their tasks from that file if it exists, so data survives an app restart. If the file doesn't exist yet, a fresh `Owner` is created instead.

Files modified to support this:

- `pawpal_system.py` — adds the `Owner.save_to_json()` and `Owner.load_from_json()` methods.
- `app.py` — loads the owner from `data.json` on startup and saves after every mutation (adding a pet, adding a task, marking a task complete).
- `.gitignore` — adds `data.json`, since it's user-generated runtime data and not something to commit.

## 🎨 Output Formatting

- **Status indicators** — ✅ (done) / ⏳ (pending), used in both `main.py` and `app.py`.
- **Priority indicators** — 🔴 (high) / 🟡 (medium) / 🟢 (low), used in both `main.py` and `app.py`.
- `main.py` uses the `tabulate` library (`tablefmt="simple"`) to render all its schedule sections as aligned tables instead of manual print loops.
- `app.py` shows the same emoji indicators inline in the task list and in the generated schedule's `st.table`.

## 📸 Demo Walkthrough

### UI features

The Streamlit app (`app.py`) lets a user:

- Enter an owner name and a pet name/species, which create `Owner` and `Pet` objects held in session state.
- Add a task with a description, time, duration, and priority.
- View the pet's current task list, with a **Mark complete** checkbox next to each pending task.
- Click **Generate schedule** to build and display the day's schedule.

### Example workflow

1. Enter an owner name (e.g. "Jordan") and a pet name/species (e.g. "Mochi", dog) — this creates the `Owner` and `Pet` behind the scenes.
2. Add a task, such as "Morning walk" at "08:00", 20 minutes, high priority. The task appears in the "Current tasks" list.
3. Add a second task at the same time (e.g. "Feed breakfast" at "08:00") to see the conflict warning later.
4. Click **Generate schedule**. The app calls `Scheduler.get_today_schedule()`, sorts the results with `Scheduler.sort_by_time()`, and runs `Scheduler.detect_conflicts()` on the sorted list.
5. Check the checkbox next to a task to mark it complete via `Pet.complete_task()`. If the task's frequency is "daily" or "weekly", `Task.next_occurrence()` fires automatically and a new row for the next occurrence appears in the task list after the page reruns.

### Key Scheduler behaviors shown

- **Sorting** — tasks in the generated schedule always appear ordered by time, regardless of the order they were added.
- **Conflict warnings** — two tasks sharing the same time (e.g. both at 08:00) each trigger an `st.warning(...)` message instead of silently overlapping; when nothing conflicts, the app shows a success message instead.
- **Recurrence** — completing a "daily" or "weekly" task doesn't just check it off; it spawns the next occurrence with `due_date` advanced by a day or a week, visible as a new row in the task list.

### Sample CLI output

Running `python main.py` produces output like:

```
=== Today's Schedule ===
[08:00] Rex - Morning walk (frequency: once, status: Pending)
[08:00] Whiskers - Feed breakfast (frequency: once, status: Pending)
[09:00] Rex - Give medication (frequency: daily, status: Pending)
[18:30] Whiskers - Clean litter box (frequency: daily, status: Pending)

=== Conflicts ===
Conflict at 08:00: Morning walk, Feed breakfast
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
