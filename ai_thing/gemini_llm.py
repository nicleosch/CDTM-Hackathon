from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path=".env")  # Make sure this is the correct path to your .env file

class GeminiLLM:
    def __init__(self, model=None):
        # Get environment variables
        api_key = os.getenv("GOOGLE_CLOUD_API")
        
        if not api_key:
            raise ValueError("API key (GOOGLE_CLOUD_API) must be set")
        
        # Set default model to the one that works in gemini_api.py
        self.model = model or "gemini-2.0-flash-001"
        
        # Print debug information
        print(f"API Key: {'Set' if api_key else 'Not set'}")
        print(f"Model: {self.model}")
        
        # Initialize the client exactly like in gemini_api.py
        self.client = genai.Client(
            vertexai=False,  # Do not use Vertex AI
            api_key=api_key
        )

    def complete(self, prompt: str) -> str:
        try:
            # Generate content from the Gemini model given a prompt (exactly like in gemini_api.py)
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            print(f"Error generating content: {str(e)}")
            return f"Error: {str(e)}"