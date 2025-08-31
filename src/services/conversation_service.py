import streamlit as st

from src.clients.interface import ApiClientInterface


class ConversationService:
    """Service to manage conversation state."""

    def __init__(self, api_client: ApiClientInterface):
        """Initialize the service."""
        self.api_client = api_client
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def handle_new_message(self, user_input: str):
        """
        Handle a new user message.

        Args:
            user_input: The message from the user.
        """
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Generate and add assistant response to chat history
        assistant_response = self.api_client.generate(user_input)
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_response}
        )
