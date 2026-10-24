import streamlit as st
import uuid

#project imports
from app.core.database import get_checkpointer
from app.graph.chat_graph import graph

def create_new_chat():
  """yo Helper Function le New Chat Banaucha Jaba User le New Conversation Click garcha"""
  
  
  #Eddi Current Chat nai Empty cha bhane New Conversation nabanaune
  
  active_chat = st.session_state.chats.get(
    st.session_state.get("active_chat_id") #esle current active chat id dincha
  )
  
  #eddi chats Find bhaena bhane "None" return garcha
  
  #Eddi chat Find bhaeko cha i.e active_chat None chaina
  #and messages = [] cha jun False ho i.e Khali cha
  #and not messages=[] garda True huncha jasle Condition True huncha
  if active_chat is not None and not active_chat["messages"]:
    return #return matra lekhda yo Function stop huncha and below ko code execute hudaina
  
  
  chat_id = str(uuid.uuid4())
  
  st.session_state.chats[chat_id] = {
    "title" : "New Conversation",
    "messages" : []
  }
  st.session_state["active_chat_id"] = chat_id
  

def get_chat_title(chat):
  
  for msg in chat.get("messages",[]):
    
    # LangGraph bata aayeko HumanMessage handle gareko
    if getattr(msg, "type", None) == "human":
      content = msg.content
    
    # Purano dictionary format pani support gareko
    elif isinstance(msg, dict) and msg.get("role") == "user":
      content = msg.get("content", "")
      
    else:
      continue
 
    
    if isinstance(content,str) :
      return content.strip()[:35]
  
  else:
    return "New Conversation"


def select_chat(chat_id):
  #select chat le chai jun chat ma click garcha tesko chat_id chai active_chat_id ma assign huncha
  st.session_state["active_chat_id"] = chat_id
  

def delete_chat(chat_id, checkpointer):
  if st.session_state["active_chat_id"] != chat_id:
    
    st.session_state.chats.pop(chat_id,None)
    #eddi chat_id key chaina bhane None return garcha
    
    checkpointer.delete_thread(chat_id)
    
    
def get_all_chats():
  checkpointer = get_checkpointer()
  
  #database ma save bhaeka Checkpoints list garne
  checkpoints = list(checkpointer.list(None))
  
  all_chats = {}
  
  for checkpoint in checkpoints:
    chat_id = checkpoint.config["configurable"]["thread_id"]
    
    if chat_id not in all_chats:
      all_chats[chat_id] = {
        
      }
    
  for chat_id in all_chats:
    
    CONFIG = {
      "configurable" : {
        "thread_id" : chat_id
      }
    }
    
    state = graph.get_state(CONFIG)
    
    all_chats[chat_id] = {
      "title" : "New Conversation",
      "messages" : state.values.get("messages",[])
    }
  
  return all_chats