import streamlit as st 
import uuid

#backend import
from app.graph.chat_graph import graph
from langchain_core.messages import HumanMessage
from app.helper.slow_stream import slow_stream_for_chunks
from app.helper.ui_helper_function import create_new_chat, get_chat_title , select_chat, delete_chat, get_all_chats
from app.graph.chat_graph import checkpointer

from pathlib import Path


#start mai 

#database bata sabai chats lyaune

if "chats" not in st.session_state:
    st.session_state.chats = get_all_chats()

#get_all_chats() khali huda {} aaucha


#active chat id assign garne

#eddi active_chat_id chaina session_state ma bhane
if "active_chat_id" not in st.session_state:
    
    #st.session_state.chats = {} huda False huncha
    if st.session_state.chats :
        
        #get_all_chats() le sabbhanda naya chat pahila dincha, tesaile reversed() chaidaina
        #next(iter(...)) le dictionary ko pahilo (sabbhanda naya) chat ko id dincha
        st.session_state.active_chat_id = next(
            iter(
                st.session_state.chats
            )
        )
    
    else:
        st.session_state.active_chat_id = None
        
#Chat select gareko chaina & database pani khali cha bhane
if st.session_state.active_chat_id is None:
    create_new_chat()



#  UI SECTION  

# Page configuration: Streamlit ko pahilo command yehi hunu parchha,
st.set_page_config(
    page_title="IntelliChat AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_NAME = "IntelliChat AI"
LOGO_PATH = Path(__file__).parent / "app" / "image" / "intellichat_ai_logo.png"

# Sidebar ko duita width: khulda 290px, collapse hunda 70px (thin icon rail)
SIDEBAR_OPEN_WIDTH = 290
SIDEBAR_RAIL_WIDTH = 70

# Icon-only button ko label khali rakhda Streamlit warning dinchha,
# tesaile ek space rakheko (icon matra dekhinchha).
ICON_ONLY = " "

ABOUT_TEXT = (
    "IntelliChat AI is an AI-powered chat interface for LLM and "
    "LangGraph-based assistants. Type your question in the box below "
    "to get started. Created by Ujjwal Dahal."
)

# Sidebar khulyo ki rail ma chha bhanera yaad rakhne (UI state matra,
# chat ko session_state sanga kehi sambandha chhaina)
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True


def toggle_sidebar():
    """Sidebar lai full <-> thin rail ma badalne."""
    st.session_state.sidebar_open = not st.session_state.sidebar_open


#  CSS 
BASE_CSS = """
<style>
:root {
    --bg: #060E22;
    --panel: #0A1630;
    --panel-hover: #102343;
    --border: #1B3154;
    --cyan: #26B8FC;
    --blue: #219BFB;
    --indigo: #5957FB;
    --purple: #8857FB;
    --white: #FCFCFC;
    --muted: #91A3C2;
}

/* Global */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--white) !important;
    font-family: "Inter", "Segoe UI", system-ui, sans-serif;
}

/* Header transparent, Deploy button / mathi ko line / menu / footer lukaune */
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stAppDeployButton"], .stDeployButton { display: none !important; }
#MainMenu, footer { visibility: hidden; }

/* Hamro afnai toggle button use garne, tesaile Streamlit ko default
   collapse/expand arrow ra resize handle lukaeko */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
[data-testid="stSidebarResizeHandle"],
div[class*="ResizeHandle"] { display: none !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #081329 0%, #060E22 100%) !important;
    border-right: 1px solid var(--border);
    transition: width .25s ease, min-width .25s ease, max-width .25s ease;
    overflow: hidden;
}
[data-testid="stSidebar"] > div:first-child {
    width: 100% !important;
    padding: 18px 12px 12px !important;
}

/* Sidebar ko buttons: transparent, hover ma cyan */
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] [data-testid="stPopover"] > div > button {
    border: 1px solid transparent !important;
    border-radius: 12px !important;
    background: transparent !important;
    color: var(--muted) !important;
    min-height: 42px;
    transition: all .18s ease;
}
[data-testid="stSidebar"] .stButton > button:hover,
[data-testid="stSidebar"] [data-testid="stPopover"] > div > button:hover {
    background: var(--panel-hover) !important;
    border-color: var(--border) !important;
    color: var(--cyan) !important;
}

/* Brand */
.brand-name {
    color: var(--white); font-size: 18px; font-weight: 750;
    letter-spacing: -0.4px; line-height: 1.1;
}
.brand-subtitle { color: var(--muted); font-size: 11px; margin-top: 3px; }
.brand-logo {
    width: 40px; height: 40px; border-radius: 12px;
    display: flex; justify-content: center; align-items: center;
    background: linear-gradient(135deg, #26B8FC, #5957FB 65%, #8857FB);
    box-shadow: 0 0 22px rgba(38, 184, 252, .18);
    color: white; font-size: 22px; font-weight: 700;
}

.sidebar-label {
    color: var(--muted); font-size: 11px; font-weight: 700;
    letter-spacing: 1.2px; text-transform: uppercase;
    margin: 22px 6px 10px;
}

/* About card (sidebar ma) */
.info-card {
    background: var(--panel); border: 1px solid var(--border);
    border-radius: 14px; padding: 14px 15px;
    color: var(--muted); font-size: 12.5px; line-height: 1.7;
}

/* Profile / avatar */
.sidebar-footer { border-top: 1px solid var(--border); padding-top: 6px; }
.profile-card { display: flex; align-items: center; gap: 10px; padding: 10px 6px 2px; }
.avatar {
    width: 36px; height: 36px; border-radius: 50%; flex-shrink: 0;
    background: linear-gradient(135deg, #219BFB, #8857FB);
    color: white; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
}
.profile-name { color: var(--white); font-size: 13px; font-weight: 650; }
.profile-plan { color: var(--muted); font-size: 11px; margin-top: 2px; }

/* Main area */
.main .block-container, [data-testid="stMainBlockContainer"] {
    max-width: 880px;
    padding-top: 40px;
    padding-bottom: 140px;
}

.welcome-title {
    text-align: center; font-size: clamp(30px, 4vw, 46px); line-height: 1.2;
    letter-spacing: -1.8px; font-weight: 800; color: var(--white);
    margin: 90px 0 0;
}
.gradient-text {
    background: linear-gradient(90deg, #26B8FC, #5957FB, #8857FB);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.welcome-description {
    text-align: center; color: var(--muted); font-size: 15px; line-height: 1.8;
    margin: 16px auto 34px; max-width: 540px;
}

/* Chat bubbles (ChatGPT jasto) */
/* Common: Streamlit ko default box hataune */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 6px 0 !important;
    margin-bottom: 18px;
    gap: 14px;
}

/* AI message: LEFT ma, bubble chhaina, avatar/emoji pani chhaina (ChatGPT ko jastai) */
[data-testid="stChatMessage"] p { line-height: 1.75; }

/* USER message: RIGHT ma, rounded gradient bubble, avatar chhaina.
   row-reverse + margin-left:auto le bubble lai dayan tira dhakelchha,
   fit-content le bubble text jati matra chaude hunchha. */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    flex-direction: row-reverse;
    width: fit-content;
    max-width: 78%;
    margin-left: auto;
    padding: 12px 18px !important;
    background: linear-gradient(135deg, rgba(38,184,252,.16), rgba(136,87,251,.16)) !important;
    border: 1px solid #1F3A66 !important;
    border-radius: 20px 20px 6px 20px !important;
    text-align: left;
}

/* User ra AI dubai ko avatar (emoji/sticker/icon) lukaune, ChatGPT ma hudaina */
[data-testid="stChatMessageAvatarUser"],
[data-testid="chatAvatarIcon-user"],
[data-testid="stChatMessageAvatarAssistant"],
[data-testid="stChatMessageAvatarAI"],
[data-testid="chatAvatarIcon-assistant"],
[data-testid="chatAvatarIcon-ai"] { display: none !important; }

/* Chat input */
[data-testid="stBottom"], [data-testid="stBottom"] > div { background: var(--bg) !important; }
[data-testid="stBottomBlockContainer"] { max-width: 880px; }

/* Streamlit le bhitra nested div ma gray rakhchha, tesaile > div ma pani rang diyeko */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div {
    background: #0A1730 !important;
    border-color: #263D62 !important;
    border-radius: 18px !important;
}
[data-testid="stChatInput"] { border: 1px solid #263D62 !important; }
[data-testid="stChatInput"] > div { border: none !important; }
[data-testid="stChatInput"]:focus-within {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 1px rgba(38, 184, 252, .18), 0 0 24px rgba(38, 184, 252, .08);
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--white) !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: var(--muted) !important; }
/* Send button: brand gradient */
[data-testid="stChatInputSubmitButton"] {
    background: linear-gradient(135deg, #26B8FC, #5957FB) !important;
    color: #fff !important; border-radius: 12px !important;
}

/* Mobile */
@media (max-width: 700px) {
    .main .block-container, [data-testid="stMainBlockContainer"] {
        padding: 24px 14px 120px;
    }
    .welcome-title { letter-spacing: -0.8px; margin-top: 50px; }
}

/* New Conversation button: gradient */
[data-testid="stSidebar"] .st-key-new_chat button,
[data-testid="stSidebar"] .st-key-rail_new button {
    background: linear-gradient(135deg, #26B8FC, #5957FB 65%, #8857FB) !important;
    color: #fff !important;
    font-weight: 650 !important;
    border: none !important;
    box-shadow: 0 6px 20px rgba(89, 87, 251, .25);
}
[data-testid="stSidebar"] .st-key-new_chat button:hover,
[data-testid="stSidebar"] .st-key-rail_new button:hover {
    filter: brightness(1.1);
    color: #fff !important;
}

/* Conversation list: title left ma, active chat highlight */
[data-testid="stSidebar"] [class*="st-key-select_"] button,
[data-testid="stSidebar"] [class*="st-key-active_select_"] button {
    justify-content: flex-start !important;
    text-align: left;
    font-size: 13.5px;
}
[data-testid="stSidebar"] [class*="st-key-active_select_"] button {
    background: var(--panel-hover) !important;
    border-color: var(--border) !important;
    color: var(--white) !important;
}

/* Delete (x) button: halka dekhaune, hover ma matra red */
[data-testid="stSidebar"] [class*="st-key-delete_"] button { color: #5d6f8f !important; }
[data-testid="stSidebar"] [class*="st-key-delete_"] button:hover { color: #ff6b6b !important; }
</style>
"""

# Sidebar ko width state anusar badlinchha (open vs rail)
WIDTH_CSS = """
<style>
[data-testid="stSidebar"] {
    width: __W__px !important;
    min-width: __W__px !important;
    max-width: __W__px !important;
}
</style>
"""

# Rail mode ma matra lagne extra CSS: buttons lai square icon button banaune
RAIL_CSS = """
<style>
/* Padding hataera sabai icon ekdam bich ma (center) rakhne */
[data-testid="stSidebar"] > div:first-child { padding: 14px 0 12px !important; }
[data-testid="stSidebarUserContent"] { padding: 0 !important; }

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.6rem !important;
    align-items: center !important;
}
[data-testid="stSidebar"] [data-testid="stElementContainer"],
[data-testid="stSidebar"] [data-testid="stImage"] {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
}

/* Sabai button (popover sahit) = 46px ko square icon button */
[data-testid="stSidebar"] button {
    width: 46px !important;
    min-width: 46px !important;
    min-height: 46px !important;
    padding: 0 !important;
    gap: 0 !important;
    justify-content: center !important;
    border-radius: 14px !important;
}
[data-testid="stSidebar"] [data-testid="stPopover"] { width: auto !important; }

/* Popover ko tala-ko chevron (v) lukaune, icon matra dekhaune */
[data-testid="stSidebar"] [data-testid="stPopover"] button > *:last-child:not(:first-child),
[data-testid="stSidebar"] [data-testid="stPopover"] button svg:last-of-type:not(:first-of-type) {
    display: none !important;
}
</style>
"""

WELCOME_HTML = """
<h1 class="welcome-title">
    Welcome to <span class="gradient-text">IntelliChat AI</span>
</h1>
<p class="welcome-description">
    Ask questions, explore ideas, and solve problems.
    Your intelligent workspace starts here.
</p>
"""

st.markdown(BASE_CSS, unsafe_allow_html=True)

is_open = st.session_state.sidebar_open
st.markdown(
    WIDTH_CSS.replace("__W__", str(SIDEBAR_OPEN_WIDTH if is_open else SIDEBAR_RAIL_WIDTH)),
    unsafe_allow_html=True,
)
if not is_open:
    st.markdown(RAIL_CSS, unsafe_allow_html=True)


#  Sidebar (sabai static, chat logic sanga kehi sambandha chhaina) 
with st.sidebar:
    if is_open:
        # Brand row: logo + name + collapse button ek linema
        logo_col, name_col, toggle_col = st.columns([1.1, 3.2, 1], vertical_alignment="center")

        with logo_col:
            if LOGO_PATH.exists():
                st.image(str(LOGO_PATH), width=40)
            else:
                st.markdown('<div class="brand-logo">✦</div>', unsafe_allow_html=True)

        with name_col:
            st.markdown(
                f'<div class="brand-name">{APP_NAME}</div>'
                '<div class="brand-subtitle">Your intelligent workspace</div>',
                unsafe_allow_html=True,
            )

        with toggle_col:
            # Click garda rail mode ma jancha
            st.button(
                ICON_ONLY,
                icon=":material/keyboard_double_arrow_left:",
                key="collapse_btn",
                help="Collapse sidebar",
                on_click=toggle_sidebar,
            )
        
        # NEW CHAT ko lagi 
        
        st.button(
          label="New Conversation",
          icon=":material/add:",
          use_container_width=True,
          key="new_chat",
          on_click=create_new_chat,
        )
        
        st.markdown('<div class="sidebar-label">Recent conversations</div>', unsafe_allow_html=True)
        
        
        # Scroll hune conversation list
        history_container = st.container(height=260, border=False)
        
        with history_container:
          
          #sabai chats 
        #  all_chats = st.session_state.get("chats",{})
        
          #database bata aayeko chats (get_all_chats() le sabbhanda naya chat pahila dincha)
          db_chats = get_all_chats()
          
          all_chats = {}
          
          #Naya khali chat (jasma message chhaina) database ma hudaina, 
          #tesaile session_state bata liyera sabbhanda mathi rakhne
          for chat_id, chat in reversed(list(st.session_state.chats.items())):
              
            if chat_id not in db_chats and not chat["messages"]:
              all_chats[chat_id] = chat
          
          #tespachi database ko chats thapne
          all_chats.update(db_chats)
          
          #all_chats pahilai naya-dekhi-purano order ma chha
          for chat_id, chat in all_chats.items():
            chat_title = get_chat_title(chat)
            
            if chat_id == st.session_state["active_chat_id"]:
              is_active = True
            else:
              is_active = False
            
            col_chat, col_delete = st.columns([5, 1], gap="small", vertical_alignment="center")
            
            with col_chat:
              # Active chat ko key ma "active_" thapeko, CSS le highlight garna
              
              st.button(
                  chat_title,
                  
                  icon=":material/chat_bubble:" if is_active else ":material/chat_bubble_outline:",
                  
                  key=f"{'active_' if is_active else ''}select_{chat_id}",
                  
                  use_container_width=True,
                  help=chat_title,
                  on_click=select_chat,
                  args=(chat_id,),
              )
              
            with col_delete:
                st.button(
                    ICON_ONLY,
                    icon=":material/close:",
                    key=f"delete_{chat_id}",
                    help="Delete conversation",
                    on_click=delete_chat,
                    args=(chat_id,checkpointer),
                )

          
          
        st.markdown('<div class="sidebar-label">About</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-card">{ABOUT_TEXT}</div>', unsafe_allow_html=True)

        # Profile card lai tala dhakelna spacer (screen height anusar)
        st.markdown('<div style="height:max(0px, calc(100vh - 520px))"></div>', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="sidebar-footer">
                <div class="profile-card">
                    <div class="avatar">U</div>
                    <div>
                        <div class="profile-name">My Workspace</div>
                        <div class="profile-plan">AI Assistant</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        # THIN ICON RAIL: symbol matra, hover garda tooltip dekhinchha
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=40)
        else:
            st.markdown(
                '<div class="brand-logo" style="margin:0 auto;">✦</div>',
                unsafe_allow_html=True,
            )
        st.write("")

        # Sidebar feri kholne button
        st.button(
            ICON_ONLY,
            icon=":material/keyboard_double_arrow_right:",
            key="expand_btn",
            help="Expand sidebar",
            on_click=toggle_sidebar,
        )
        
        #collapse garesi "New Conversation" ko Symbol
        st.button(
          ICON_ONLY, 
          icon=":material/add:", 
          key="rail_new", 
          help="New Conversation", 
          on_click=create_new_chat
          )

        # About: rail ma thau na hunale popover ma
        with st.popover(ICON_ONLY, icon=":material/info:", help="About IntelliChat AI"):
            st.markdown(f"**{APP_NAME}**")
            st.caption(ABOUT_TEXT)

        st.markdown('<div style="height:max(0px, calc(100vh - 400px))"></div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="sidebar-footer"><div class="profile-card" '
            'style="justify-content:center;padding-left:0;padding-right:0;">'
            '<div class="avatar">U</div></div></div>',
            unsafe_allow_html=True,
        )


# Functionaly Code yaa cha
  
CONFIG = {
    "configurable" : {
      "thread_id" : st.session_state["active_chat_id"]
    }
  }


active_chat_id = st.session_state.get("active_chat_id")

#active_chat_id None huna sakcha so 
active_chat = (
    st.session_state.chats.get(active_chat_id)
    
    if active_chat_id
    else None
)

# Chat select nabhayeko awastha handle gareko
if active_chat is None:
    st.info("Select a conversation or create a new one.")
    st.stop()

each_chat_msg_history = active_chat["messages"]



# UI ONLY: chat khali hunda welcome screen dekhaune. st.empty() placeholder
# use gareko, taki pahilo message pathaun bittikai tala ko line le hataidina sakos.

welcome_placeholder = st.empty()
if not each_chat_msg_history:
  with welcome_placeholder.container():
    st.markdown(WELCOME_HTML, unsafe_allow_html=True)


# LangChain message objects ra purana dictionaries dubai render gareko
for msg in each_chat_msg_history:
    
    if isinstance(msg, dict):
        role = msg.get("role")
        content = msg.get("content", "")
    else:
        role = getattr(msg, "type", "")
        content = getattr(msg, "content", "")

    if role in ("user", "human"):
        with st.chat_message("user"):
            st.write(content)

    elif role in ("ai", "assistant"):
        with st.chat_message("assistant"):
            st.write(content)


user_query = st.chat_input("Ask IntelliChat AI")

if user_query:
  # welcome_placeholder.empty()  # UI ONLY: message aayepachi welcome screen hataune
  
  each_chat_msg_history.append({
  "role" : "user",
  "content" : user_query
  })
   
  
  with st.chat_message(name="user"):
    st.write(user_query)
    
  with st.chat_message("ai"):
    
      # # Loading indicator ko lagi placeholder banaune
      # #st.empty() euta place ma bhaeko content lai pachi replace garna milcha
      
      # loading = st.empty()
      # loading.markdown("Thinking...")


      # Graph bata streaming chunks line
      stream_result = graph.stream(
          {
              "messages": [
                HumanMessage(content=user_query)
                ]
          },
          stream_mode="messages",
          config=CONFIG
      )


      ai_answer = st.write_stream(
        slow_stream_for_chunks(stream_result)
      )

      # Complete AI response history ma save garne
      if ai_answer:
          each_chat_msg_history.append({
              "role": "ai",
              "content": ai_answer
          })
  
  #Jawaf save bhayepachi page feri refresh garne, 
  #taki sidebar ma chat ko title (pahilo message) turuntai dekhos
  st.rerun()