import os

import streamlit as st

from dev.mocks.mock_ollama_client import MockOllamaApiClient
from src.clients.ollama_api_client.client import OllamaApiClient
from src.components.chat_ui import render_chat_messages
from src.components.sidebar import render_sidebar
from src.services.conversation_service import ConversationService


def initialize_session():
    """Initialize the session state."""
    if (
        "conversation_service" not in st.session_state
        or st.session_state.conversation_service is None
    ):
        # Check DEBUG environment variable to decide which client to use
        debug_mode = os.getenv("DEBUG", "false").lower() == "true"

        if debug_mode:
            api_client = MockOllamaApiClient()
        else:
            try:
                api_client = OllamaApiClient()
            except ValueError:
                # Fallback to mock client if environment variables are not configured
                api_client = MockOllamaApiClient()

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
