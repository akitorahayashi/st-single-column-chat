from abc import ABC, abstractmethod
from typing import Optional


class OllamaClientInterface(ABC):
    """Interface for Ollama client implementations."""

    @abstractmethod
    def generate(self, prompt: str, model: str = None) -> Optional[str]:
        """
        Generate text using the Ollama model.

        Args:
            prompt: The prompt to send to the model.
            model: The name of the model to use for generation.

        Returns:
            The generated text from the model, or None if an error occurs.
        """
        pass
