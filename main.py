from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from chatbot import ask
from pdf_gen import generate_pdf
from ocr import extract_invoice
import io

app = FastAPI()

# --- Feature 1: Chatbot ---
class Query(BaseModel):
    question: str
    csv_path: str = "data.csv"

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/chat")
def chat(query: Query):
    answer = ask(query.question, query.csv_path)
    return {"answer": answer}

# --- Feature 2: PDF ---
class FormData(BaseModel):
    name: str
    date: str
    items: list[dict]

@app.post("/generate-pdf")
def create_pdf(data: FormData):
    pdf_bytes = generate_pdf(data.dict())
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=report.pdf"}
    )

# --- Feature 3: OCR ---
@app.post("/ocr")
async def ocr_invoice(file: UploadFile = File(...)):
    contents = await file.read()
    result = extract_invoice(contents, file.filename)
    return result

from email_pdf import fetch_and_convert

@app.post("/email-to-pdf")
def email_to_pdf():
    results = fetch_and_convert()
    return {"processed": results}