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

- No structural changes yet — this section will be updated in later phases if the implementation reveals gaps (e.g., additional helper methods on `Scheduler` needed to talk to `Owner`/`Pet`).

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
