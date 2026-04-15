import os
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def load_csv(path: str) -> str:
    df = pd.read_csv(path)
    return df.to_string(index=False)  # converts CSV to plain text

def ask(question: str, csv_path: str) -> str:
    context = load_csv(csv_path)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"Answer questions using this data:\n{context}"},
            {"role": "user",   "content": question}
        ]
    )
    return response.choices[0].message.content