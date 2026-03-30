# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My main 3 actions that users were to be able to do were create a list of pet care tasks, have the list ordered by priority or length of the task's time, and make a weekly layout for easy visualization. The main objects, attributes, and methods needed were: 
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

It considered priority and then time, making sure the high priority tasks came first, and then ordered the tasks based on the amount of time it would take. I decided that priority would matter the most because things like giving pets their important medication or first meal of the day would matter more than any quick task in general. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
One tradeoff could be that it creates individual checklists for each pet. It doesn't combine the lists of both pets together. If there are many pets, it may become an incredibly long list that is hard to search. However, this ensures the owner has clear view of which pet needs what, rather than potentially mixing up which task has been done for which pet when doing things in the schedule. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used it as a partner throughout this project, thinking of my own ideas and taking the instructions from the project, and then inputting them into Claude. Evaluating the code that it generates each time, I would make sure that it looked reasonable before implementing. Upon adding a phase of changes, I would then test the app to see how it runs, and ask Claude to make adjustments accordingly. 
**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

There was one part where Claude was about to allow numerous owners in the app. However, this app is specifically meant in my plans to be designed for one user and their multiple or single pet. The change was going to take the app in a complete different direction as a larger monitor system than what I intended as a personal app, so I reclarified my prompt. I evaluated by looking at the code and the brief summary that Claude provides at the end of its code generation. 
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

The behaviors I tested were sorting based on priority, recurring tasks, conflict overlaps, and having multiple pets. These tests are crucial to making sure the schedule would function without issues, as they are all behaviors that would fail and inconvenience the user if not behaving correctly.  
**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am highly confident that the schedule works correctly, as I tested it with a couple tasks, and used filters to generate the schedules. I also tested have numerous pets to view how the schedule would look. An edge case I would test next time seeing if a task that is the same name as another task can be removed without influencing or causing all of the tasts of the same name to be removed.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with the generate schedule function, which was able to create a schedule based on the filter selected. It was able to form schedules that were arranged based on priority or duration which was something I was aiming highly to do. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would want to make the weekly task a constantly-open standard 7 day calendar view instead of 7 individual drop downs, as it can get in the way when users are trying to quickly view and then get to taking care of their pets. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Something I learned/solidified is that AI is able to act as a partner, assisting you in creating projects. However, checking its work must always be done, as it may generate unwanted details/ideas. Thoroughly checking, working on prompt engineering, and brainstorming small details here and there will allow you to use AI to perform high capabilities.