import streamlit as st
import uuid
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="IntelliChat AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_NAME = "IntelliChat AI"
LOGO_PATH = Path(__file__).parent / "app" / "image" / "intellichat_ai_logo.png"



# Sidebar ko duita width: khulda 290px, collapse hunda 68px (thin icon rail)
SIDEBAR_OPEN_WIDTH = 290
SIDEBAR_RAIL_WIDTH = 70


# Icon-only button ko label khali rakhda Streamlit warning dinchha,
# tesaile ek space rakheko (icon matra dekhinchha).
ICON_ONLY = " "


# Session state (tapai ko original logic same chha)
if "chats" not in st.session_state:
    first_chat_id = str(uuid.uuid4())
    st.session_state.chats = {
        first_chat_id: {"title": "New conversation", "messages": []}
    }
    st.session_state.active_chat = first_chat_id

if "active_chat" not in st.session_state:
    st.session_state.active_chat = next(iter(st.session_state.chats))

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# NAYA (UI matra): sidebar khulyo ki rail mode ma chha bhanera yaad rakhna
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def create_new_chat():
    """Create a new chat and make it active."""
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {"title": "New conversation", "messages": []}
    st.session_state.active_chat = chat_id
    st.session_state.pending_prompt = None


def delete_chat(chat_id):
    """Delete a chat and select another available chat."""
    st.session_state.chats.pop(chat_id, None)

    if not st.session_state.chats:
        create_new_chat()
    elif st.session_state.active_chat == chat_id:
        st.session_state.active_chat = next(iter(st.session_state.chats))

    st.session_state.pending_prompt = None


def generate_response(prompt, history):
    """
    Replace this placeholder with your LangGraph or LLM invocation.
    The current function only demonstrates the UI.
    """
    return (
        f"You asked: **{prompt}**\n\n"
        "This is a UI demonstration response. Connect your AI backend "
        "to generate real answers."
    )


def toggle_sidebar():
    """Sidebar lai full <-> thin rail ma badalne."""
    st.session_state.sidebar_open = not st.session_state.sidebar_open


def toggle_view(name):
    """
    Settings / About panel on-off garne.
    Ek choti ek matra panel khulos bhanera arko lai band gareko
    (pahila dubai ek sathai True huna sakthyo).
    """
    other = "show_about" if name == "show_settings" else "show_settings"
    st.session_state[name] = not st.session_state.get(name, False)
    st.session_state[other] = False


# ---------------------------------------------------------------------------
# Styling
# Color theme tapai ko jastai rakheko (same CSS variables).
# ---------------------------------------------------------------------------
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

/* Header transparent: top ma kaalo patti naaune */
[data-testid="stHeader"] { background: transparent !important; }

/* "Deploy" button ra mathi ko patli line lukaune (chat app ma chaidaina) */
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stAppDeployButton"], .stDeployButton { display: none !important; }

/* Streamlit ko default menu/footer lukaune */
#MainMenu, footer { visibility: hidden; }

/* Hamro afnai toggle button use garne, tesaile Streamlit ko default
   collapse/expand arrow lukaeko (natra duita toggle dekhinthyo) */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
[data-testid="stSidebarResizeHandle"],
div[class*="ResizeHandle"] { display: none !important; }

/* ---------- Sidebar (common) ---------- */
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

/* Sidebar ko sabai buttons: dark card style */
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] [data-testid="stPopover"] > div > button {
    border: 1px solid transparent !important;
    border-radius: 12px !important;
    background: transparent !important;
    color: var(--muted) !important;
    min-height: 42px;
    transition: all .18s ease;
    justify-content: flex-start;
    text-align: left;
    font-size: 13.5px !important;
}
[data-testid="stSidebar"] .stButton > button:hover,
[data-testid="stSidebar"] [data-testid="stPopover"] > div > button:hover {
    background: var(--panel-hover) !important;
    border-color: var(--border) !important;
    color: var(--cyan) !important;
}

/* Primary "New chat" button: gradient (brand color) */
.st-key-new_chat button, .st-key-rail_new button {
    background: linear-gradient(135deg, #26B8FC, #5957FB 65%, #8857FB) !important;
    color: #fff !important;
    font-weight: 650 !important;
    border: none !important;
    box-shadow: 0 6px 20px rgba(89, 87, 251, .25);
}
.st-key-new_chat button:hover, .st-key-rail_new button:hover {
    filter: brightness(1.1);
    color: #fff !important;
}

/* Active conversation highlight */
.chat-active button {
    background: var(--panel-hover) !important;
    border-color: var(--border) !important;
    color: var(--white) !important;
}

/* Delete (x) button halka dekhaune, hover ma matra red */
[class*="st-key-delete_"] button { color: #5d6f8f !important; }
[class*="st-key-delete_"] button:hover { color: #ff6b6b !important; }

/* ---------- Brand ---------- */
.brand-name {
    color: var(--white);
    font-size: 18px;
    font-weight: 750;
    letter-spacing: -0.4px;
    line-height: 1.1;
}
.brand-subtitle { color: var(--muted); font-size: 11px; margin-top: 3px; }
.brand-logo {
    width: 40px; height: 40px; border-radius: 12px;
    display: flex; justify-content: center; align-items: center;
    background: linear-gradient(135deg, #26B8FC, #5957FB 65%, #8857FB);
    box-shadow: 0 0 22px rgba(38, 184, 252, .18);
    color: white; font-size: 22px; font-weight: 700;
}

.sidebar-history-label {
    color: var(--muted); font-size: 11px; font-weight: 700;
    letter-spacing: 1.2px; text-transform: uppercase;
    margin: 18px 6px 8px;
}

/* ---------- Profile / avatar ---------- */
.sidebar-footer { border-top: 1px solid var(--border); margin-top: 10px; padding-top: 6px; }
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

.top-label {
    color: var(--cyan); text-transform: uppercase; letter-spacing: 2.5px;
    font-size: 11px; font-weight: 750; text-align: center; margin: 40px 0 16px;
}
.welcome-title {
    text-align: center; font-size: clamp(30px, 4vw, 46px); line-height: 1.2;
    letter-spacing: -1.8px; font-weight: 800; color: var(--white); margin: 0;
}
.gradient-text {
    background: linear-gradient(90deg, #26B8FC, #5957FB, #8857FB);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.welcome-description {
    text-align: center; color: var(--muted); font-size: 15px; line-height: 1.8;
    margin: 16px auto 34px; max-width: 540px;
}
.section-label {
    color: #B8C7DF; font-size: 12px; font-weight: 700;
    letter-spacing: 1.2px; text-transform: uppercase; margin: 8px 0 12px;
}

/* Suggestion cards (main area ko buttons) */
[class*="st-key-suggest_"] button {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    color: var(--white) !important;
    min-height: 96px;
    padding: 16px 18px !important;
    justify-content: flex-start !important;
    text-align: left !important;
    transition: all .2s ease;
}
/* Button bhitra ko text lai column ma rakhne: title mathi, description tala.
   Pahila sabai ek line ma "..." sanga katiyeko thiyo (nowrap/ellipsis) */
[class*="st-key-suggest_"] button > div,
[class*="st-key-suggest_"] button [data-testid="stMarkdownContainer"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: flex-start !important;
    width: 100%;
}
[class*="st-key-suggest_"] button p {
    display: block !important;
    width: 100%;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    text-align: left !important;
    font-size: 13.5px; line-height: 1.55; color: var(--muted); margin: 0;
}
[class*="st-key-suggest_"] button p:first-child {
    color: var(--white); font-weight: 650; font-size: 14.5px; margin-bottom: 6px;
}
[class*="st-key-suggest_"] button:hover {
    border-color: var(--cyan) !important;
    background: var(--panel-hover) !important;
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(38, 184, 252, .08);
}

/* Settings / About "Back to chat" jasta main buttons */
.main .stButton > button {
    border: 1px solid var(--border); border-radius: 10px;
    background: #0D1B35; color: var(--white);
}
.main .stButton > button:hover { border-color: var(--cyan); color: var(--cyan); }

/* ---------- Chat bubbles ---------- */
[data-testid="stChatMessage"] {
    background: #0A1730 !important;
    border: 1px solid #15294A;
    border-radius: 16px !important;
    padding: 16px 18px !important;
    margin-bottom: 14px;
}
/* User message lai halka alag rang (brand tint) */
[data-testid="stChatMessage"]:has([data-testid*="User"]) {
    background: linear-gradient(135deg, rgba(38,184,252,.08), rgba(136,87,251,.08)) !important;
    border-color: #1F3A66;
}

/* ---------- Chat input ---------- */
[data-testid="stBottom"], [data-testid="stBottom"] > div { background: var(--bg) !important; }

/* Input box content area (880px) sanga mileko width */
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
    .welcome-title { letter-spacing: -0.8px; }
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
/* Rail ma padding hataera sabai icon ekdam bich ma (center) rakhne */
[data-testid="stSidebar"] > div:first-child { padding: 14px 0 12px !important; }
[data-testid="stSidebarUserContent"] { padding: 0 !important; }

/* Icon haru ko bich ko gap sano + sabai center */
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

st.markdown(BASE_CSS, unsafe_allow_html=True)

is_open = st.session_state.sidebar_open
st.markdown(
    WIDTH_CSS.replace("__W__", str(SIDEBAR_OPEN_WIDTH if is_open else SIDEBAR_RAIL_WIDTH)),
    unsafe_allow_html=True,
)
if not is_open:
    st.markdown(RAIL_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:

    if is_open:
        # ===================== FULL SIDEBAR =====================
        # Brand row: logo + name + collapse button ek linema
        # (purano code ma <div> alag-alag st.markdown ma khulera banda gareko
        # thiyo, Streamlit ma tyo kaam gardaina; tesaile columns use gareko)
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

        st.write("")  # sano gap

        if st.button(
            "New chat",
            icon=":material/add:",
            use_container_width=True,
            key="new_chat",
        ):
            create_new_chat()
            st.rerun()

        st.markdown(
            '<div class="sidebar-history-label">Recent conversations</div>',
            unsafe_allow_html=True,
        )

        # Scroll hune conversation list
        history_container = st.container(height=370, border=False)

        with history_container:
            # Naya chat sabbhanda mathi
            for chat_id, chat in reversed(list(st.session_state.chats.items())):
                title = chat["title"]
                short_title = title[:24] + "..." if len(title) > 24 else title
                is_active = chat_id == st.session_state.active_chat

                col_chat, col_delete = st.columns([5, 1], gap="small", vertical_alignment="center")

                with col_chat:
                    # Active chat lai alag highlight dina wrapper class
                    if is_active:
                        st.markdown('<div class="chat-active">', unsafe_allow_html=True)
                    if st.button(
                        short_title,
                        icon=":material/chat_bubble:" if is_active else ":material/chat_bubble_outline:",
                        key=f"select_{chat_id}",
                        use_container_width=True,
                        help=title,
                    ):
                        st.session_state.active_chat = chat_id
                        st.rerun()
                    if is_active:
                        st.markdown("</div>", unsafe_allow_html=True)

                with col_delete:
                    if st.button(
                        ICON_ONLY,
                        icon=":material/close:",
                        key=f"delete_{chat_id}",
                        help="Delete conversation",
                    ):
                        delete_chat(chat_id)
                        st.rerun()

        # Footer: history ko muni, tala fixed jasto basne
        st.markdown('<div class="sidebar-footer">', unsafe_allow_html=True)

        if st.button("Settings", icon=":material/settings:", use_container_width=True, key="settings_btn"):
            toggle_view("show_settings")
            st.rerun()

        if st.button("About IntelliChat AI", icon=":material/info:", use_container_width=True, key="about_btn"):
            toggle_view("show_about")
            st.rerun()

        st.markdown(
            """
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
        # ===================== THIN ICON RAIL =====================
        # Yaha text hudaina, symbol matra. Har icon ma help= (tooltip) diyeko
        # jasle hover garda k ho bhanera dekhaucha.

        # Brand logo (chhoto) - rail ko mathi ma
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

        # New chat (gradient icon button)
        if st.button(ICON_ONLY, icon=":material/add:", key="rail_new", help="New chat"):
            create_new_chat()
            st.rerun()

        # Chat history: popover ma list dekhaune (rail ma thau na hunale)
        with st.popover(ICON_ONLY, icon=":material/history:", help="Recent conversations"):
            st.caption("Recent conversations")
            for chat_id, chat in reversed(list(st.session_state.chats.items())):
                title = chat["title"]
                short_title = title[:28] + "..." if len(title) > 28 else title
                prefix = ":material/chat_bubble:" if chat_id == st.session_state.active_chat else ":material/chat_bubble_outline:"
                if st.button(
                    short_title,
                    icon=prefix,
                    key=f"rail_select_{chat_id}",
                    use_container_width=True,
                    help=title,
                ):
                    st.session_state.active_chat = chat_id
                    st.rerun()

        # Footer icon haru lai tala dhakelna spacer
        st.markdown('<div style="height:max(0px, calc(100vh - 620px))"></div>', unsafe_allow_html=True)

        if st.button(ICON_ONLY, icon=":material/settings:", key="rail_settings", help="Settings"):
            toggle_view("show_settings")
            st.rerun()

        if st.button(ICON_ONLY, icon=":material/info:", key="rail_about", help="About IntelliChat AI"):
            toggle_view("show_about")
            st.rerun()

        st.markdown(
            '<div class="sidebar-footer"><div class="profile-card" '
            'style="justify-content:center;padding-left:0;padding-right:0;">'
            '<div class="avatar">U</div></div></div>',
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Main panel (functionality tapai ko original jastai)
# ---------------------------------------------------------------------------
active_chat = st.session_state.chats[st.session_state.active_chat]
messages = active_chat["messages"]

if st.session_state.get("show_settings", False):
    st.markdown("## Settings")
    st.caption("Basic application settings")
    st.selectbox("Response style", ["Balanced", "Concise", "Detailed"])
    if st.button("Back to chat"):
        st.session_state.show_settings = False
        st.rerun()

elif st.session_state.get("show_about", False):
    st.markdown("## About IntelliChat AI")
    st.write(
        "IntelliChat AI is a chat interface designed for connecting "
        "LLMs and LangGraph-based assistants."
    )
    if st.button("Back to chat"):
        st.session_state.show_about = False
        st.rerun()

else:
    # Welcome screen: chat khali hunda matra dekhaune
    if not messages:
        st.markdown(
            """
            <div class="top-label">✦ Intelligent conversations, simplified</div>
            <h1 class="welcome-title">
                Welcome to <span class="gradient-text">IntelliChat AI</span>
            </h1>
            <p class="welcome-description">
                Ask questions, explore ideas, and solve problems.
                Your intelligent workspace starts here.
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="section-label">Try asking</div>', unsafe_allow_html=True)

        prompts = [
            ("⌘", "Explain a complex topic", "Explain how large language models work in simple terms."),
            ("✧", "Help me write code", "Help me write clean and readable Python code."),
            ("↗", "Explore new ideas", "Give me a structured plan to learn a new technical skill."),
            ("◎", "Summarize information", "Show me a practical method to summarize a long document."),
        ]

        prompt_cols = st.columns(2, gap="medium")

        for index, (symbol, title, prompt) in enumerate(prompts):
            with prompt_cols[index % 2]:
                if st.button(
                    f"{symbol}  {title}\n\n{prompt}",
                    key=f"suggest_{index}",
                    use_container_width=True,
                ):
                    st.session_state.pending_prompt = prompt
                    st.rerun()

    # Purana messages dekhaune (avatar thapeko: user vs assistant chinna sajilo)
    for message in messages:
        avatar = ":material/person:" if message["role"] == "user" else ":material/auto_awesome:"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Chat input + suggested prompt handling
    typed_prompt = st.chat_input("Message IntelliChat AI...")

    prompt = st.session_state.pending_prompt or typed_prompt
    st.session_state.pending_prompt = None

    if prompt:
        messages.append({"role": "user", "content": prompt})

        if active_chat["title"] == "New conversation":
            active_chat["title"] = prompt[:35]

        with st.chat_message("user", avatar=":material/person:"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=":material/auto_awesome:"):
            with st.spinner("Thinking..."):
                answer = generate_response(prompt, messages)
            st.markdown(answer)

        messages.append({"role": "assistant", "content": answer})
        st.rerun()