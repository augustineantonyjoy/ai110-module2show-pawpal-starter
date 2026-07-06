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

I split AI collaboration across two tools with different jobs. Claude Code (CLI) acted as the "lead architect" — reading the assignment requirements, breaking the six phases into individual checklist steps, writing precise implementation prompts one step at a time, and independently verifying each result (reading the diff, running `pytest`, running `main.py`, and even simulating the Streamlit UI with `AppTest` to click buttons and check for exceptions) before moving on. The actual code changes were written by the Claude extension inside VS Code, working from those prompts.

Going one small step at a time — rather than handing over a whole phase at once — was the most helpful pattern. Narrow, specific prompts (e.g., "implement these exact method bodies, don't change signatures") produced code that matched the intended design on the first try far more often than broad prompts would have. Using a fresh chat session for the Phase 4 algorithm brainstorming (separate from the implementation chat) also kept that planning discussion from getting mixed into unrelated context.

**b. Judgment and verification**

When reviewing `Scheduler.filter_tasks()`, I asked the AI whether the method could be simplified. It proposed collapsing two sequential `if` blocks into a single list comprehension with combined boolean conditions — functionally identical, and technically avoiding one intermediate list allocation. I rejected it: the performance gain was negligible at this app's scale, while the original two-step version ("filter by pet, then by status") was easier to read at a glance than the more compact but denser comprehension. I verified this wasn't just a style preference by confirming the two versions were behaviorally equivalent, then made the readability-vs-performance tradeoff call explicitly rather than assuming "more Pythonic" meant "better" (documented in section 2b).

More generally, I didn't treat "the code runs" as sufficient verification — every phase was checked by actually executing something: unit tests, the CLI demo, or a simulated UI interaction, not just a read-through of the diff.

---

## 4. Testing and Verification

**a. What you tested**

The automated suite (`tests/test_pawpal.py`) covers five behaviors: marking a task complete, adding a task to a pet, chronological sorting of an out-of-order task list, daily recurrence (completing a "daily" task correctly spawns a new occurrence with `due_date` advanced by one day), and conflict detection (two tasks at the same time are flagged). These were chosen because they're the core promises the whole app makes to a user — if sorting, recurrence, or conflict detection silently broke, the schedule itself would become untrustworthy, which is the one thing this app can't afford to get wrong.

Beyond automated tests, I also verified behavior manually at every phase: running `main.py` to see real CLI output, and using Streamlit's `AppTest` to simulate clicking "Add task," "Mark complete," and "Generate schedule" in the actual `app.py` to confirm the UI wiring (not just the backend classes in isolation) worked end-to-end, since a passing unit test doesn't guarantee the Streamlit integration is correct.

**b. Confidence**

⭐⭐⭐⭐ (4/5). All 5 tests pass and I additionally confirmed the UI itself behaves correctly through simulated interaction, so I'm confident the core scheduling logic is correct for the scenarios it was built for. It's not a 5 because the suite doesn't yet cover some edge cases: weekly recurrence specifically (only daily is unit-tested), filtering behavior, a pet with zero tasks, or two recurring tasks with different frequencies interacting in the same conflict check.

If I had more time, I'd add tests for: weekly recurrence, `filter_tasks()` with both `pet_name` and `completed` set simultaneously, an empty task list passed to `sort_by_time`/`detect_conflicts`, and conflicts across two different pets (not just within one pet's task list).

---

## 5. Reflection

**a. What went well**

The recurrence feature (`Task.next_occurrence()` / `Pet.complete_task()`) is what I'm most satisfied with — it required a real design change mid-project (adding `due_date`, deciding which class should own the behavior) rather than just filling in a stub, and I could verify it working correctly all the way through: unit test, CLI output, and live in the Streamlit UI.

**b. What you would improve**

Given another iteration, I'd address the gaps identified in section 4b — particularly testing weekly recurrence and multi-pet conflict detection — and revisit `filter_tasks()`'s `id()`-based approach for identifying tasks, which works but is a workaround for `Task` not being hashable; a cleaner design might give `Task` a unique `id` field instead of relying on Python object identity.

**c. Key takeaway**

Acting as the "lead architect" meant my job wasn't writing code line-by-line, it was deciding *what* to build, in what order, and how to verify each piece before trusting it — the AI was fast at producing correct-looking code, but only checking behavior (tests, running the app, simulating clicks) caught the difference between code that looks right and code that actually is right.
