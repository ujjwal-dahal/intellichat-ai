from langgraph.graph import START, END , StateGraph

#adding tools in LangGraph
from langgraph.prebuilt import ToolNode , tools_condition

from app.state.chat_state import ChatState
from app.node.chat_node import chat_node
from app.core.database import get_checkpointer
from app.node.chat_node import ALL_TOOLS

checkpointer = get_checkpointer()

builder = StateGraph(ChatState)

#node
builder.add_node("chat_node",chat_node)
builder.add_node("tools",ToolNode(ALL_TOOLS))

#edge
builder.add_edge(START,"chat_node")

builder.add_conditional_edges(
  "chat_node",
  
  tools_condition
)

builder.add_edge("tools","chat_node")

#compile
graph = builder.compile(checkpointer=checkpointer)