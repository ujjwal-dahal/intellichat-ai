from langgraph.graph import START, END , StateGraph

from app.state.chat_state import ChatState
from app.node.chat_node import chat_node
from app.core.database import get_checkpointer

checkpointer = get_checkpointer()

builder = StateGraph(ChatState)

#node
builder.add_node("chat_node",chat_node)

#edge
builder.add_edge(START,"chat_node")
builder.add_edge("chat_node",END)

#compile
graph = builder.compile(checkpointer=checkpointer)