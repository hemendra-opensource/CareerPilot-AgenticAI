import json
import re
import logging
from utils.groq_client import GroqClient

class LLMService:
    """Service to handle all LLM interactions through Groq."""
    
    def __init__(self):
        self.client = GroqClient()
        
    def generate_text(self, prompt: str) -> str:
        """
        Generates a plain text response.
        
        Args:
            prompt: The text prompt for the model.
            
        Returns:
            The generated text response.
        """
        return self.client.generate_response(prompt)
        
    def generate_json(self, prompt: str, schema_description: str = "") -> dict:
        """
        Generates a JSON response from the LLM.
        Appends JSON formatting instructions and parses the response.
        
        Args:
            prompt: The core text prompt.
            schema_description: Outline of the target JSON structure.
            
        Returns:
            A dictionary containing the parsed JSON content.
        """
        json_prompt = (
            prompt + 
            f"\n\nRespond ONLY with a valid JSON object matching the following schema/description:\n"
            f"{schema_description}\n"
            f"Do not include any conversational intro/outro, markdown formatting tags, "
            f"backticks (like ```json), or explanation outside the JSON itself."
        )
        
        response_text = self.client.generate_response(json_prompt)
        
        # Clean any backticks or markdown wrapper if the model generates them
        cleaned_text = response_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        elif cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
            
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
            
        cleaned_text = cleaned_text.strip()
        
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            # Fallback: regex extraction of JSON block
            logging.warning("JSON parsing failed, attempting regex fallback extraction.")
            match = re.search(r"\{.*\}", cleaned_text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    pass
            
            # Return failure details for upstream handlers
            return {
                "error": "Failed to parse JSON response from LLM",
                "raw_response": response_text
            }
