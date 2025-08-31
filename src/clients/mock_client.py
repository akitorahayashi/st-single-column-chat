from src.clients.interface import ApiClientInterface


class MockApiClient(ApiClientInterface):
    """Mock API client."""

    def generate(self, user_input: str) -> str:
        """Generate a response from the user's input."""
        return f"AIが返す: {user_input}"
