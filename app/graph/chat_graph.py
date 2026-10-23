from langgraph.graph import START, END , StateGraph
from langgraph.checkpoint.memory import InMemorySaver

from app.state.chat_state import ChatState
from app.node.chat_node import chat_node

checkpointer = InMemorySaver()

builder = StateGraph(ChatState)

#node
builder.add_node("chat_node",chat_node)

#edge
builder.add_edge(START,"chat_node")
builder.add_edge("chat_node",END)

#compile
graph = builder.compile(checkpointer=checkpointer)