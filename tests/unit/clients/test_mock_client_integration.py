import unittest
from unittest.mock import MagicMock, patch

from dev.mocks.mock_ollama_client import MockOllamaApiClient
from src.services.conversation_service import ConversationService


class TestMockClientIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = MockOllamaApiClient()

    def test_mock_client_generate_basic(self):
        """Test basic text generation with mock client."""
        # Arrange
        prompt = "Hello, how are you?"

        # Act
        response = self.mock_client.generate(prompt)

        # Assert
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
        self.assertIn("モック応答", response)
        self.assertIn(prompt[:30], response)

    def test_mock_client_custom_responses(self):
        """Test custom responses for specific inputs."""
        test_cases = [
            ("fsfs", "（fsfs に対するモック応答）"),
            ("こんにちは", "こんにちは！元気ですか？"),
            ("hello", "Hello! How can I help you?"),
            ("test", "テスト用のモック応答です。"),
            ("テスト", "これはテスト応答です。"),
        ]

        for prompt, expected_response in test_cases:
            with self.subTest(prompt=prompt):
                # Act
                response = self.mock_client.generate(prompt)

                # Assert
                self.assertEqual(response, expected_response)

    def test_mock_client_rotating_responses(self):
        """Test that mock client rotates through default responses."""
        # Arrange
        prompt = "some random input"
        responses = []

        # Act - Generate multiple responses
        for _ in range(6):  # More than the number of mock responses
            response = self.mock_client.generate(prompt)
            responses.append(response)

        # Assert - Should cycle through responses
        self.assertEqual(len(responses), 6)
        # First response should be different from second, but first should equal sixth (cycling)
        self.assertNotEqual(responses[0], responses[1])
        # Response should contain the mock response pattern
        for response in responses:
            self.assertIn("モック応答", response)

    @patch("streamlit.session_state", new_callable=MagicMock)
    def test_integration_with_conversation_service(self, mock_session_state):
        """Test integration of mock client with ConversationService."""
        # Arrange
        mock_session_state.messages = []
        service = ConversationService(self.mock_client)
        user_input = "test message"

        # Act
        service.handle_new_message(user_input)

        # Assert
        self.assertEqual(len(mock_session_state.messages), 2)
        self.assertEqual(mock_session_state.messages[0]["role"], "user")
        self.assertEqual(mock_session_state.messages[0]["content"], user_input)
        self.assertEqual(mock_session_state.messages[1]["role"], "assistant")
        # Response should contain mock response pattern
        self.assertIn("モック応答", mock_session_state.messages[1]["content"])

    def test_mock_client_with_model_parameter(self):
        """Test that mock client ignores model parameter."""
        # Arrange
        prompt = "hello"
        model = "some-model"

        # Act
        response_with_model = self.mock_client.generate(prompt, model)
        response_without_model = self.mock_client.generate(prompt)

        # Assert - Both should return the same custom response
        self.assertEqual(response_with_model, response_without_model)
        self.assertEqual(response_with_model, "Hello! How can I help you?")

    @patch("time.sleep")
    def test_mock_client_simulates_delay(self, mock_sleep):
        """Test that mock client simulates API delay."""
        # Arrange
        prompt = "some input"

        # Act
        self.mock_client.generate(prompt)

        # Assert - Should call sleep to simulate delay
        mock_sleep.assert_called_once_with(2)

    @patch("time.sleep")
    def test_mock_client_custom_response_short_delay(self, mock_sleep):
        """Test that custom responses have shorter delay."""
        # Arrange
        prompt = "hello"

        # Act
        self.mock_client.generate(prompt)

        # Assert - Custom responses should have shorter delay
        mock_sleep.assert_called_once_with(0.5)


if __name__ == "__main__":
    unittest.main()
