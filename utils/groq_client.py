from groq import Groq
from config.config import Config

class GroqClient:
    """Handles communication with the Groq API using the official Groq SDK."""
    
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model_name = Config.GROQ_MODEL
        self.initialized = False
        
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
            self.initialized = True

    def generate_response(self, prompt: str) -> str:
        """
        Generates a text response from the Groq model using the provided prompt.
        
        Args:
            prompt: The input prompt for the model.
            
        Returns:
            The generated text response.
        """
        if not self.initialized:
            raise ValueError("Groq Client is not initialized. Please set your GROQ_API_KEY in the .env file.")
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model_name,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error communicating with Groq API: {str(e)}"

    def test_connection(self) -> tuple[bool, str]:
        """
        Verifies communication with the Groq API.
        
        Returns:
            A tuple of (success_status, status_message).
        """
        if not self.initialized:
            return False, "Groq Client is not configured. Missing API Key."
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": "Say 'Success' in one word.",
                    }
                ],
                model=self.model_name,
            )
            output = chat_completion.choices[0].message.content.strip()
            if "Success" in output or output:
                return True, f"Connection successful! Model response: '{output}'"
            return False, "Received empty response from Groq API."
        except Exception as e:
            return False, f"Connection test failed: {str(e)}"
