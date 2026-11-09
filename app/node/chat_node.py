from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from app.state.chat_state import ChatState
from app.core.config import setting

#all tools
from app.tools.weather_tool import weather_tool
from app.tools.search_tool import tavily_search_tool
from app.tools.calculator_tool import calculator_tool


from app.helper.all_mcp_tools import get_all_mcp_tools
from app.prompt.system_prompt import SYSTEM_PROMPT

ALL_TOOLS = get_all_mcp_tools()

# ALL_TOOLS = [
#   weather_tool,
#   tavily_search_tool,
#   calculator_tool
# ]


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
  