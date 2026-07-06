# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My design centers on four classes: `Task`, `Pet`, `Owner`, and `Scheduler`.

- `Task` is a simple data holder for a single care activity: `description`, `time` (HH:MM string), `frequency` ("once"/"daily"/"weekly"), and a `completed` flag, plus a `mark_complete()` method.
- `Pet` stores a pet's `name` and `species` and owns a list of its `Task`s, with `add_task()` and `get_tasks()`.
- `Owner` manages a list of `Pet`s and can aggregate every task across all of their pets via `get_all_tasks()`.
- `Scheduler` is the "brain" of the system. It holds a reference to an `Owner` and is responsible for all cross-cutting logic that doesn't belong to any single pet: building the day's schedule, sorting by time, filtering by pet/status, and detecting scheduling conflicts.

I kept `Task` and `Pet` as Python dataclasses since they're mostly data with a couple of small behaviors, which keeps the code concise per the project's guidance.

**b. Design changes**

- Added a `due_date` field to `Task` (defaulting to today) that wasn't in the original design. It became necessary once I implemented recurring tasks in Phase 4 — without a date, there was nothing for a "daily" or "weekly" task to advance by `timedelta`.
- Added `Pet.complete_task()` rather than putting completion/recurrence logic on `Scheduler`. Since a `Task` already belongs to a specific `Pet`, it made more sense for the `Pet` to own the responsibility of marking a task done and appending its next occurrence, keeping `Scheduler` focused purely on cross-pet operations (sorting, filtering, conflict detection).

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The `Scheduler` considers four constraints:

- **Time**: `sort_by_time()` orders tasks chronologically by their `time` (HH:MM) attribute so the owner sees the day in order.
- **Pet / completion status**: `filter_tasks()` narrows the list down to a specific pet's tasks and/or only pending/completed ones, so an owner isn't overwhelmed by every task for every pet at once.
- **Frequency**: `Task.next_occurrence()` (called from `Pet.complete_task()`) automatically regenerates "daily"/"weekly" tasks so recurring care (feeding, meds) doesn't have to be manually re-entered.
- **Time collisions**: `detect_conflicts()` flags when two tasks land on the exact same time, which matters most for a single owner juggling multiple pets' schedules.

I prioritized time and conflicts first since a schedule that's out of order or silently double-books a time slot is the most immediately confusing to a user; filtering and recurrence were the next layer of convenience on top of a correct base schedule.

**b. Tradeoffs**

One tradeoff: I asked my AI coding assistant to review `Scheduler.filter_tasks()` for simplification. It suggested combining the two sequential `if` blocks (filter by pet, then filter by completion) into a single list comprehension with combined boolean conditions, avoiding one intermediate list allocation.

I rejected this suggestion and kept the original two-step version. The performance gain is negligible at this scale (a handful of tasks per pet), while the original's step-by-step narrowing ("first filter by pet, then by status") is easier to read at a glance than a single comprehension with `(x is None or ...) and (y is None or ...)` logic. This is a case where the more "Pythonic" version traded away readability for a performance gain the app doesn't need — I chose clarity since this is a learning project meant to be read by graders/reviewers, not a hot path.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
