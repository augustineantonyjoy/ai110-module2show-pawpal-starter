# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

For the "Advanced Algorithmic Capability" stretch feature, I asked the agent to add a third scheduling capability beyond the base sorting/filtering/conflict-detection/recurrence requirements: a "next available slot" finder that, given a desired duration, returns the first open time gap in a pet's schedule. This required adding a real `duration_minutes` field to `Task` (previously the Streamlit UI collected a duration input but never stored it), implementing the gap-finding algorithm on `Scheduler`, wiring the UI input through, and demonstrating/testing it.

**What did the agent do?**

- Added `duration_minutes: int = 30` to the `Task` dataclass in `pawpal_system.py`.
- Implemented `Scheduler.find_next_available_slot(tasks, duration_minutes, day_start, day_end)`, which converts tasks into busy `(start, end)` intervals in minutes-since-midnight, sorts them, and scans forward from `day_start` for the first sufficiently large gap.
- Updated `app.py` so the existing "Duration (minutes)" input is actually passed into `Task(...)` instead of being discarded.
- Added a demo block to `main.py` printing the result of a 45-minute slot search, and a new `tests/test_pawpal.py::test_find_next_available_slot` covering both a normal gap-finding case and a fully-booked-day case (asserting `None`).
- Updated `README.md` with a "Next Available Slot" section describing the algorithm and a sample CLI output.

**What did you have to verify or fix manually?**

I ran the new method against five manual scenarios (a simple gap, a request too large for the first gap, a fully booked day, an empty task list, and unsorted input) to confirm correctness before trusting it — all five behaved correctly.

More importantly, verifying this way caught a real bug the agent introduced without realizing it: `duration_minutes` was added to `Task`, but `Owner.save_to_json()`/`Owner.load_from_json()` (from the Data Persistence stretch feature, built earlier) were never updated to include the new field. A round-trip save/load was silently resetting every task's `duration_minutes` back to the default `30`, which would have quietly broken the new slot-finder for any task with a non-default duration. I caught this only by explicitly testing a save→load round-trip with a non-default duration, not by reading the diff — the code looked correct at a glance since the new field itself worked fine in isolation. I sent the agent back to add `duration_minutes` to both the serialization and deserialization logic, then re-verified the round-trip before accepting the change.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
