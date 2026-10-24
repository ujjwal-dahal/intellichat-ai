import streamlit as st
import uuid


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
  
  for msg in chat["messages"]:
    if msg["role"] == "user":
     chat_title = msg["content"]

    
    if len(chat_title) < 35:
      return chat_title
    
    return chat_title[:35]
  
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
    