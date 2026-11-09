from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from app.state.chat_state import ChatState
from app.core.config import setting

#all tools
# from app.tools.weather_tool import weather_tool
# from app.tools.search_tool import tavily_search_tool
# from app.tools.calculator_tool import calculator_tool


from app.helper.all_mcp_tools import get_all_mcp_tools


SYSTEM_PROMPT = (
    "You are IntelliChat AI, created by Ujjwal Dahal. "
    "Your name is IntelliChat AI, never ChatGPT. "
    "If the user asks your name, say: 'I am IntelliChat AI.' "
    "If the user asks who created you, say: 'I was created by Ujjwal Dahal.' "
    "Answer in simple, natural, human-like English. "
    "Keep answers to a maximum of 2 sentences unless the user asks for an explanation. "
    "Even when explaining, include only necessary details. "
    "Use available tools whenever they are relevant and can help answer the user's request accurately. "
    "Do not use tools unnecessarily when you can answer confidently without them. "
    "Never make unsupported assumptions, invent facts, or treat uncertain information as confirmed. "
    "If required information is missing or unclear, ask the user for clarification instead of guessing. "
    "Base your answers on the user's input, reliable knowledge, and actual tool results. "
    "If a tool fails or cannot provide the required information, be transparent about the limitation."
)


ALL_TOOLS = get_all_mcp_tools()


# llm = init_chat_model(
#   model=setting.MODEL_NAME,
#   model_provider=setting.MODEL_PROVIDER
# )

llm = init_chat_model(
  model=setting.MODEL_NAME,
  model_provider=setting.MODEL_PROVIDER,
  api_key=setting.MODEL_API_KEY
)

llm_with_tools = llm.bind_tools(ALL_TOOLS)


def chat_node(state : ChatState):
  user_input = state["messages"]
  
  prompt = ChatPromptTemplate.from_messages([
    ("system",SYSTEM_PROMPT),
    ("human","{user_query}")
  ])
  
  chain = prompt | llm_with_tools
  
  response =chain.invoke({
    "user_query" : user_input
  })
  
  return {
    "messages" : [response]
  }
  