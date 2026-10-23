from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from app.state.chat_state import ChatState
from app.core.config import setting

 


SYSTEM_PROMPT = (
    "You are IntelliChat AI, created by Ujjwal Dahal. "
    "Your name is IntelliChat AI, never ChatGPT. "
    "If the user asks your name, say: 'I am IntelliChat AI.' "
    "If the user asks who created you, say: 'I was created by Ujjwal Dahal.' "
    "Answer in simple, natural, human-like English. "
    "Keep answers to a maximum of 2 sentences unless the user asks for an explanation. "
    "Even when explaining, include only necessary details."
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
  