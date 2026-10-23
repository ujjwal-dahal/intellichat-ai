session_state = {
    "chats": {
        "chat_id_1": {
            "title": "What is Python?",
            "messages": [
                {
                    "role": "user",
                    "content": "What is Python?"
                },
                {
                    "role": "assistant",
                    "content": "Python is a programming language."
                }
            ]
        },

        "chat_id_2": {
            "title": "Learn LangGraph",
            "messages": [
                {
                    "role": "user",
                    "content": "What is LangGraph?"
                },
                {
                    "role": "assistant",
                    "content": "LangGraph helps build stateful AI workflows."
                }
            ]
        }
    },

    "active_chat": "chat_id_1",

    "pending_prompt": "Explain Python simply",

    "sidebar_open": True,

    "show_settings": False,

    "show_about": False
}

# print(f"Chats in Session Chat : {session_state["chats"]}")
print(next(iter(session_state["chats"])))