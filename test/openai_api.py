import os
import dotenv
from openai import OpenAI

# Load environment variables from .env file
dotenv.load_dotenv()

# Get the OpenAI API key
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found in environment variables")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

def get_completion(prompt, model="gpt-4o-2024-11-20"):
    """
    Get a completion from the OpenAI API.
    
    Args:
        prompt (str): The prompt to send to the API.
        model (str, optional): The model to use. Defaults to "gpt-3.5-turbo".
    
    Returns:
        str: The completion text.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    prompt = "What can you do to help me with Python programming?"
    completion = get_completion(prompt)
    print(completion)