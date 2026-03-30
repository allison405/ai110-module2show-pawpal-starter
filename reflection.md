# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My main 3 actions that users were to be able to do were create a list of pet care tasks, have the list ordered by priority, and make a weekly layout for easy visualization. The main objects, attributes, and methods needed were: 
Task: 
    Attributes:
    title — name of the task (e.g., "Morning walk")
    duration_minutes — how long it takes
    priority — "low", "medium", or "high"
    day_of_week — which day(s) it applies to (for weekly layout)
    notes — optional extra info (e.g., "use leash")

    Methods:
    to_dict() — convert to dictionary for display/storage
    __repr__() — human-readable string version

TaskList: 
    Attributes:
    tasks — list of Task objects

    Methods:
    add_task(task) — add a new task
    remove_task(title) — remove by name
    get_by_priority() — return tasks sorted high → low 
    get_by_day(day) - return tasks for a specific day

WeeklySchedule
Attributes:
schedule — a dict mapping day names to lists of tasks 

Methods:
assign_task(task, day) — place a task on a specific day
get_day(day) — retrieve all tasks for that day
display() — return the full week as a structured format for Streamlit

Pet
Attributes:
name
species (dog, cat, etc.)
task_list — the TaskList associated with this pet

Owner
Attributes:
name
pet — their Pet object

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, after asking claude about potential missing components and bottlenecks, I implemented changes that it suggested. An example was that it found that if tasks had the same name and you decided to remove the task by a title string, it would remove all of the same tasks. So instead, it added a new unique ID field for each task so that removal is more specific towards one task instead of all tasks of the same name.
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
