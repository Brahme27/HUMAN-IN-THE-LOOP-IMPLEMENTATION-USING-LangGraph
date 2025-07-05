# This Repo Practically Explains These Three Topics

## **1. Human-in-the-Loop (HITL) in Workflow**

> Think of it like this: the LLM is doing a task, but it **pauses** and asks a human:
> “Hey, should I continue with what I plan to do, or do you want to change anything?”

* In your workflow, HITL happens **before the assistant (LLM) runs**.
* This gives you a chance to **check or update the input** before the LLM takes action.
* It's like adding a manual review step in an automated process.

## **2. Editing Human Feedback in Workflow**

> Sometimes the user says something, and the assistant starts working—but then the user says:
> “Wait! That’s not what I meant. Let me correct it.”

* You can **edit the user message after it's already submitted**.
* This is done using `graph.update_state()` with a **new user message**.
* Then, you **resume the workflow** and it continues using the updated input.

Example:
User said: `"multiply 2 and 3"`
But later changes it to: `"multiply 15 and 6"`
→ You update the state, and the assistant now works on the corrected question.

## **3. Runtime Human Feedback in Workflow**

> This is more interactive. The assistant pauses mid-process and waits for a human to give **new instructions** on the spot.

* You add a node called `human_feedback` in the workflow.
* Before continuing, the graph **stops at that node** and lets the user **give live input** (using `input()` or similar).
* Once feedback is received, the assistant continues with that **updated or clarified instruction**.

Example:
The assistant reaches a point, and you get asked:
“Tell me how you want to update the state”
→ You type in a new message, and the assistant picks up from there.

### Summary Table

| Concept                      | What It Does                                     | When It Happens            |
| ---------------------------- | ------------------------------------------------ | -------------------------- |
| **HITL (Human-in-the-Loop)** | Pauses before LLM runs, lets human review        | Before assistant runs      |
| **Editing Human Feedback**   | Lets you change the input after assistant starts | Midway (after input given) |
| **Runtime Human Feedback**   | Lets user give live feedback at a special node   | During graph execution     |