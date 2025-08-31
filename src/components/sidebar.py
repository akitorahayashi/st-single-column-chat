import streamlit as st


def clear_chat_history():
    """Clear chat history from session state."""
    st.session_state.messages = []
    st.session_state.conversation_service = None


def render_sidebar():
    """Render the sidebar with a new chat button."""
    with st.sidebar:
        st.title("Menu")
        st.button("New Chat", on_click=clear_chat_history)
