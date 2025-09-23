import html
from pathlib import Path

import streamlit as st
import toml


def load_chat_colors():
    """Load chat colors from config.toml"""
    config_path = Path(".streamlit/config.toml")
    if config_path.exists():
        config = toml.load(config_path)
        theme_config = config.get("theme", {})
        chat_config = config.get("chat", {})
        return {
            "user_color": chat_config.get("userMessageColor", "#262730"),
            "ai_color": chat_config.get("aiMessageColor", "#3A3B40"),
            "text_color": theme_config.get("textColor", "#FAFAFA"),
        }
    return {
        "user_color": "#262730",
        "ai_color": "#3A3B40",
        "text_color": "#FAFAFA",
    }


def render_user_message(message):
    """Render user message with inline styles"""
    colors = load_chat_colors()
    return f"""
    <style>
    .user-message {{
        display: flex;
        align-items: flex-start;
        justify-content: flex-end;
        margin: 10px 0;
    }}
    .user-content {{
        background-color: {colors['user_color']};
        color: white;
        max-width: 70%;
        padding: 12px 16px;
        border-radius: 20px;
        word-wrap: break-word;
    }}
    </style>
    <div class="user-message">
        <div class="user-content">
            {html.escape(message).replace(chr(10), '<br>')}
        </div>
    </div>
    """


def render_ai_message(message):
    """Render AI message with inline styles"""
    colors = load_chat_colors()
    return f"""
    <style>
    .ai-message {{
        display: flex;
        align-items: flex-start;
        justify-content: flex-start;
        margin: 10px 0;
    }}
    .ai-content {{
        background-color: {colors['ai_color']};
        color: {colors['text_color']};
        max-width: 70%;
        padding: 12px 16px;
        border-radius: 20px;
        word-wrap: break-word;
    }}
    </style>
    <div class="ai-message">
        <div class="ai-content">
            {html.escape(message).replace(chr(10), '<br>')}
        </div>
    </div>
    """


def render_thinking_bubble():
    """Render AI thinking bubble with inline styles"""
    colors = load_chat_colors()
    return f"""
    <style>
    .thinking-message {{
        display: flex;
        align-items: flex-start;
        justify-content: flex-start;
        margin: 10px 0;
    }}
    .thinking-content {{
        background-color: {colors['ai_color']};
        color: {colors['text_color']};
        max-width: 70%;
        padding: 12px 16px;
        border-radius: 20px;
    }}
    .thinking-dots {{
        animation: thinking 1.5s infinite;
    }}
    @keyframes thinking {{
        0%, 50%, 100% {{ opacity: 1; }}
        25%, 75% {{ opacity: 0.5; }}
    }}
    </style>
    <div class="thinking-message">
        <div class="thinking-content">
            <div style="display: flex; align-items: center;">
                <div class="thinking-dots">
                    Thinking...
                </div>
            </div>
        </div>
    </div>
    """


def render_chat_messages(messages):
    """Render all chat messages with inline styles"""
    st.markdown(
        """
    <style>
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 16px;
    }
    </style>
    <div class="chat-container">
    """,
        unsafe_allow_html=True,
    )

    for i, msg in enumerate(messages):
        # Use unique keys to prevent flickering
        if msg["role"] == "user":
            html_content = render_user_message(msg["content"])
        else:
            html_content = render_ai_message(msg["content"])

        # Use a container with unique key to prevent re-rendering
        with st.container():
            st.markdown(html_content, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
