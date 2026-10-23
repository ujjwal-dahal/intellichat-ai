from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from app.state.chat_state import ChatState
from app.core.config import setting

 
SYSTEM_PROMPT = (
    "Answer the user's question clearly and directly in a maximum of 2 sentences. "
    "Keep the answer short, simple, and easy to understand. "
    "Do not include unnecessary details or explanations."
)

llm = init_chat_model(
  model=setting.MODEL_NAME,
  model_provider=setting.MODEL_PROVIDER,
  api_key = setting.MODEL_API_KEY
)


def chat_node(state : ChatState):
  user_input = state["messages"]
  
  prompt = ChatPromptTemplate.from_messages([
    ("system",SYSTEM_PROMPT),
    ("human","{user_query}")
  ])
  
  chain = prompt | llm
  
  response = chain.invoke({
    "user_query" : user_input
  })
  
  return {
    "messages" : [response]
  }
  