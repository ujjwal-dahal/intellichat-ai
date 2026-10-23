from typing import Annotated , List ,TypedDict
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage


class ChatState(TypedDict):
  messages : Annotated[List[BaseMessage],add_messages]