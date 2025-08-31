from abc import ABC, abstractmethod


class ApiClientInterface(ABC):
    """API client interface."""

    @abstractmethod
    def generate(self, user_input: str) -> str:
        """Generate a response from the user's input."""
        pass
