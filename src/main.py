import streamlit as st

from src.clients.mock_client import MockApiClient
from src.components.chat_ui import render_chat_messages
from src.components.sidebar import render_sidebar
from src.services.conversation_service import ConversationService


def initialize_session():
    """Initialize the session state."""
    if (
        "conversation_service" not in st.session_state
        or st.session_state.conversation_service is None
    ):
        api_client = MockApiClient()
        st.session_state.conversation_service = ConversationService(api_client)


def main():
    """Main function to run the app."""
    st.title("Single Column Chat")

    initialize_session()
    render_sidebar()
    render_chat_messages()

    user_input = st.chat_input("メッセージを入力")
    if user_input:
        service: ConversationService = st.session_state.conversation_service
        service.handle_new_message(user_input)
        st.rerun()


if __name__ == "__main__":
    main()
