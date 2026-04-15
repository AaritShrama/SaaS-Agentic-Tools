import os
import base64
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_invoice(file_bytes: bytes, filename: str) -> dict:
    # Convert image to base64
    encoded = base64.b64encode(file_bytes).decode("utf-8")

    # Detect image type from filename
    ext = filename.split(".")[-1].lower()
    mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}
    mime_type = mime_map.get(ext, "image/jpeg")

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{encoded}"
                        }
                    },
                    {
                        "type": "text",
                        "text": (
                            "This is an invoice. Extract these fields and return ONLY valid JSON, nothing else:\n"
                            '{"vendor": "", "date": "", "total": "", "items": [{"name": "", "amount": ""}]}'
                        )
                    }
                ]
            }
        ]
    )

    import json
    raw = response.choices[0].message.content.strip()
    # Strip markdown code blocks if model wraps in ```json
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)