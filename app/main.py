import streamlit as st 
import uuid

#backend import
from app.graph.chat_graph import graph
from langchain_core.messages import HumanMessage


# UI ko lagi matra 
from pathlib import Path

#  UI SECTION  
# Page configuration
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


# ---------- CSS ----------
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

/* ---------- Global ---------- */
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

/* ---------- Sidebar ---------- */
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

/* ---------- Main area ---------- */
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

/* ---------- Chat bubbles ---------- */
[data-testid="stChatMessage"] {
    background: #0A1730 !important;
    border: 1px solid #15294A;
    border-radius: 16px !important;
    padding: 16px 18px !important;
    margin-bottom: 14px;
}
/* User message: halka brand tint */
[data-testid="stChatMessage"]:has([data-testid*="User"]) {
    background: linear-gradient(135deg, rgba(38,184,252,.08), rgba(136,87,251,.08)) !important;
    border-color: #1F3A66;
}
/* AI avatar: brand gradient, user avatar: halka panel */
[data-testid="stChatMessageAvatarAssistant"],
[data-testid="stChatMessageAvatarAI"] {
    background: linear-gradient(135deg, #26B8FC, #5957FB 65%, #8857FB) !important;
    color: #fff !important;
}
[data-testid="stChatMessageAvatarUser"] {
    background: var(--panel-hover) !important;
    color: var(--cyan) !important;
}

/* ---------- Chat input ---------- */
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

/* ---------- Mobile ---------- */
@media (max-width: 700px) {
    .main .block-container, [data-testid="stMainBlockContainer"] {
        padding: 24px 14px 120px;
    }
    .welcome-title { letter-spacing: -0.8px; margin-top: 50px; }
}
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



#Functionality Logic ho yaa dekhi
if "chats" not in st.session_state:
  
  #persistence
  chat_id = str(uuid.uuid4())
  st.session_state["active_chat_id"] = chat_id
  
  st.session_state.chats = {}
  
  if chat_id not in st.session_state.chats:
    st.session_state.chats[chat_id] = {
        "messages" : []
      }
  
config = {
    "configurable" : {
      "thread_id" : st.session_state["active_chat_id"]
    }
  }

active_chat = st.session_state.chats[st.session_state["active_chat_id"]]
each_chat_msg_history = active_chat["messages"]

# UI ONLY: chat khali hunda welcome screen dekhaune. st.empty() placeholder
# use gareko, taki pahilo message pathaun bittikai tala ko line le hataidina sakos.
welcome_placeholder = st.empty()
if not each_chat_msg_history:
  with welcome_placeholder.container():
    st.markdown(WELCOME_HTML, unsafe_allow_html=True)


for msg in each_chat_msg_history:
  if msg["role"] == "user":
    with st.chat_message("user"):
      st.write(msg["content"])
  
  if msg["role"] == "ai":
    with st.chat_message("ai"):
      st.write(msg["content"])


user_query = st.chat_input("Ask IntelliChat AI")

if user_query:
  welcome_placeholder.empty()  # UI ONLY: message aayepachi welcome screen hataune
  
  
  each_chat_msg_history.append({
  "role" : "user",
  "content" : user_query
  })
  
  
  with st.chat_message(name="user"):
    st.write(user_query)
    
  result = graph.invoke(
    input={
      "messages" : [HumanMessage(content=user_query)]
    }, config=config
  )

  ai_answer = result["messages"][-1].content 

  if ai_answer:
    each_chat_msg_history.append({
      "role" : "ai",
      "content" : ai_answer
    })
    
    with st.chat_message("ai"):
      st.write(ai_answer)