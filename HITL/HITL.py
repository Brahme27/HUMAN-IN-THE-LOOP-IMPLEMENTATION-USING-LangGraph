# ✅ 1. Load Environment & Initialize LLM

from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()  # Load environment variables from .env

# Set the Groq API Key
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize the LLM with LLaMA 3 (70B)
llm = ChatGroq(model="llama-3.3-70b-versatile")

# Optional: Simple test
llm.invoke("Hello")


# ✅ 2. Define Custom Arithmetic Tools

def multiply(a: int, b: int) -> int:
    """Multiply a and b"""
    return a * b

def add(a: int, b: int) -> int:
    """Add a and b"""
    return a + b

def divide(a: int, b: int) -> float:
    """Divide a by b"""
    return a / b

# List of tools for LLM usage
tools = [add, multiply, divide]


# ✅ 3. Bind Tools to LLM

llm_with_tools = llm.bind_tools(tools)


# ✅ 4. Setup LangGraph Workflow with Assistant & Tools

from IPython.display import Image, display
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, START, StateGraph, END
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# Define assistant's system role
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs")

# Define the assistant node (LLM response)
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


# ✅ 5. Build and Visualize Basic Graph

builder = StateGraph(MessagesState)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

# Save state between runs
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# Show workflow graph
display(Image(graph.get_graph().draw_mermaid_png()))


# ✅ 6. Add Interrupt to Pause Before Assistant Executes

memory = MemorySaver()
graph = builder.compile(checkpointer=memory, interrupt_before=["assistant"])
display(Image(graph.get_graph().draw_mermaid_png()))


# ✅ 7. Run the Graph with Input

thread = {"configurable": {"thread_id": 123}}
initial_input = {"messages": HumanMessage(content="Multiply 2 and 3")}

# Stream response step-by-step
for event in graph.stream(initial_input, thread, stream_mode="values"):
    event["messages"][-1].pretty_print()

# View current state
state = graph.get_state(thread)
print("Next node:", state.next)

# Continue the graph from current state
for event in graph.stream(None, thread, stream_mode="values"):
    event["messages"][-1].pretty_print()


# ✅ 8. Edit Human Feedback and Re-run

# New thread for clean demo
thread = {"configurable": {"thread_id": 1}}
initial_input = {"messages": HumanMessage(content="multiply 2 and 3")}

for event in graph.stream(initial_input, thread, stream_mode="values"):
    event["messages"][-1].pretty_print()

# Update with user feedback (edit message)
graph.update_state(thread, {"messages": [HumanMessage(content="No please multiply 15 and 6")]})

# View updated state messages
new_state = graph.get_state(thread).values
for m in new_state["messages"]:
    m.pretty_print()

# Continue execution
for event in graph.stream(None, thread, stream_mode="values"):
    event["messages"][-1].pretty_print()


# ✅ 9. Runtime Human Feedback Node (More Interactive)

# Redefine system message
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs")

# Dummy human feedback node for now (can customize later)
def human_feedback(state: MessagesState):
    pass

# Rebuild graph with feedback node
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_node("human_feedback", human_feedback)

builder.add_edge(START, "human_feedback")
builder.add_edge("human_feedback", "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "human_feedback")

# Compile with interruption before feedback
memory = MemorySaver()
graph = builder.compile(interrupt_before=["human_feedback"], checkpointer=memory)

# Display updated graph
display(Image(graph.get_graph().draw_mermaid_png()))

# Run graph again
initial_input = {"messages": HumanMessage(content="multiply 2 and 3")}
thread = {"configurable": {"thread_id": 12}}

for event in graph.stream(initial_input, thread, stream_mode="values"):
    event["messages"][-1].pretty_print()


# ✅ 10. Take Runtime Input from User to Update State

# Take new input from user
user_input = input("Tell me how you want to update the state: ")

# Update graph state at human_feedback node
graph.update_state(thread, {"messages": user_input}, as_node="human_feedback")

# Continue the flow with new input
for event in graph.stream(None, thread, stream_mode="values"):
    event["messages"][-1].pretty_print()