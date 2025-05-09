import base64
from mistralai import Mistral

def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def process_image_with_mistral(image_path):
    # Step 1: Encode the image to base64
    base64_image = encode_image(image_path)
    if not base64_image:
        return

    # Step 2: Set up Mistral API
    api_key = "rjJ4ryG5vr1g0y6bConpAKbZrCWdScja"  # Replace with your actual API key
    model = "mistral-small-latest"

    if not api_key:
        raise ValueError("API key not found. Set the API key in the script.")

    client = Mistral(api_key=api_key)

    # Step 3: Define the messages
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Extract and return only the laboratory name, date, patient name, and patient address in strict JSON format."
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                }
            ]
        }
    ]

    # Step 4: Get the chat response using strict JSON schema
    try:
        chat_response = client.chat.complete(
            model=model,
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "LabReportInfo",
                    "description": "Extracted information from a lab report.",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "laboratory_name": {"type": "string"},
                            "date": {"type": "string"},
                            "patient_name": {"type": "string"},
                            "patient_address": {"type": "string"}
                        },
                        "required": ["laboratory_name", "date", "patient_name", "patient_address"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        )
        print("\nExtracted lab report info (strict JSON format):")
        print(chat_response.choices[0].message.content)
    except Exception as e:
        print(f"Error processing image with Mistral: {e}")

if __name__ == "__main__":
    # Replace with the path to your image file
    image_path = "resources/photo_2025-05-09 23.08.49.jpeg"
    process_image_with_mistral(image_path)
