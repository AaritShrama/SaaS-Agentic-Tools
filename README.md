# AI Automation & Full-Stack Suite
This repository contains a comprehensive suite of AI-driven automation tools designed for Intelligent Document Processing (IDP), Retrieval-Augmented Generation (RAG), and automated workflow orchestration. The project implements end-to-end solutions for common business bottlenecks, including spreadsheet querying, invoice data extraction, and multi-channel document generation.
+4

## 🚀 Key Features

  1. RAG-Based Spreadsheet Chatbot: A chatbot architecture utilizing LangChain and OpenAI to perform Retrieval-Augmented Generation over structured CSV/Google Sheets data.
  2. Intelligent Bill Reading (OCR): A pipeline built to extract data from both handwritten and printed invoices using AI-based OCR.
  3. Automated Email-to-PDF: A custom IMAP workflow that captures incoming emails and renders them into structured PDF reports.
  4. Dynamic Form-to-PDF Generation: A document automation system that converts form data into professional PDFs using ReportLab and Jinja2 templates.


## 🛠️ Tech Stack

  Languages: Python (Pandas, Requests, FastAPI).

  AI/ML: OpenAI API, LangChain, AI-based OCR (IDP).

  Automation: API Orchestration, IMAP scripts, and headless browser rendering.

  Tools: GitHub, Jinja2, and environment-based configuration (.env).

## 📂 Project Structure

  chatbot.py: Logic for the RAG-based query engine.

  ocr.py: Implementation for AI-powered invoice data extraction.

  email_pdf.py: Automated email fetching and processing logic.

  pdf_gen.py: Report generation engine utilizing Jinja2 templates.

  main.py: The central FastAPI/Flask orchestrator connecting the pipelines.

  templates/: HTML templates for consistent PDF styling.

## ⚙️ Setup & Installation

1 .Clone the Repository:
Bash
git clone https://github.com/AaritShrama/SaaS-Agentic-Tools.git

2. Environment Configuration:
  Create a .env file in the root directory and add your API credentials:
    GROQ_API_KEY=your_key_here
    IMAP_USER=your_email_here
    IMAP_PASS=your_app_password_here
    Install Dependencies:

3. Bash
  pip install -r requirements.txt

## 🛡️ Security & Best Practices
  Environment Safety: Sensitive keys and credentials are managed via .env and are strictly excluded from version control via .gitignore.
  Clean Orchestration: The project structure adheres to professional standards by excluding build artifacts (__pycache__) and local virtual environments (myenv/).
