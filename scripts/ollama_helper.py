"""
ollama_helper.py
-------------------
LangChain helper functions to invoke Ollama models.
The models are hosted on a remote ubuntu server, and invoked from a Windows PC.

Requirements:
- langchain, langchain-ollama, langchain-core

"""

from langchain_ollama import OllamaLLM, ChatOllama
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Optional, Generator
import requests

# ------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
OLLAMA_HOST = "http://192.168.4.97:11434"  # Replace with your Ollama server's IP and port
OLLAMA_MODEL = "llama3.2"  # Replace with your Ollama model name
DEFAULT_TIMEOUT = 30  # Default timeout for API requests in seconds

# ------------------------------------------------------------------
# Helper Classes and Functions
# ------------------------------------------------------------------

class OllamaHelper:
    """
    A Helper class to interact with Ollama models on a remote server using LangChain.
    """

    def __init__(
        self,
        base_url: str = OLLAMA_HOST,
        model: str = OLLAMA_MODEL,
        timeout: int = DEFAULT_TIMEOUT,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ):
        self.base_url = base_url.strip("/")  # Ensure no trailing slash
        self.model = model
        self.timeout = timeout
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Base LLM (plain text generation)
        self.llm = OllamaLLM(
            host=self.base_url,
            model=self.model,
            timeout=self.timeout,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        # Chat LLM (for conversational interactions)
        self.chat_llm = ChatOllama(
            host=self.base_url,
            model=self.model,
            timeout=self.timeout,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        self.parser = StrOutputParser()

    def ask(self, question: str) -> str:
        """
        Send a plain question and get a text response.
        """
        try:
            response = self.llm.invoke(question)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama server: {e}")
            return "Error: Unable to communicate with Ollama server."
        
    def __repr__(self):
        return f"OllamaHelper(model={self.model}, host={self.base_url})"

    def list_models(self) -> list[str]:
        """
        List available models on the Ollama server.
        """
        try:
            url = f"{self.base_url}/v1/models"
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return [data]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching models from Ollama server: {e}")
            return []

if __name__ == "__main__":
    # Example usage
    helper = OllamaHelper(
        base_url=OLLAMA_HOST,
        model=OLLAMA_MODEL,
        timeout=DEFAULT_TIMEOUT
    )
    print("="*40)
    print(f"Ollama Helper initialized with model: {helper.model}")
    print("="*40)
    print("Available models on Ollama server:")
    models = helper.list_models()
    print("="*40)