import unittest
from unittest.mock import MagicMock, patch

from src.clients.interface import ApiClientInterface
from src.services.conversation_service import ConversationService


class MockApiClient(ApiClientInterface):
    def generate(self, user_input: str) -> str:
        return f"Mock response to: {user_input}"


class TestConversationService(unittest.TestCase):
    @patch("streamlit.session_state", new_callable=MagicMock)
    def test_handle_new_message(self, mock_session_state):
        # Arrange
        mock_session_state.messages = []
        mock_api_client = MockApiClient()
        # Spy on the generate method
        mock_api_client.generate = MagicMock(wraps=mock_api_client.generate)
        service = ConversationService(api_client=mock_api_client)
        user_input = "Hello, AI!"

        # Act
        service.handle_new_message(user_input)

        # Assert
        # Check if the message history was updated correctly
        self.assertEqual(len(mock_session_state.messages), 2)
        self.assertEqual(mock_session_state.messages[0]["role"], "user")
        self.assertEqual(mock_session_state.messages[0]["content"], user_input)
        self.assertEqual(mock_session_state.messages[1]["role"], "assistant")
        self.assertEqual(
            mock_session_state.messages[1]["content"], "Mock response to: Hello, AI!"
        )

        # Check if the API client was called correctly
        mock_api_client.generate.assert_called_once_with(user_input)


if __name__ == "__main__":
    unittest.main()
