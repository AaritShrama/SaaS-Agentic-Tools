import imaplib
import email
from email.header import decode_header
import os
import io
import re
import html
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


load_dotenv()

def decode_mime_header(header_value) -> str:
    """Safely decodes email headers, handling 'unknown-8bit' and other encoding errors."""
    if not header_value:
        return ""
    
    try:
        parts = decode_header(header_value)
    except Exception:
        return str(header_value)

    decoded_str = ""
    for content, charset in parts:
        if isinstance(content, bytes):
            
            if not charset or charset.lower() == 'unknown-8bit':
                charset = 'utf-8'
            
            try:
                decoded_str += content.decode(charset, errors="ignore")
            except (LookupError, TypeError):
                # Ultimate fallback to utf-8 if charset is invalid
                decoded_str += content.decode("utf-8", errors="ignore")
        else:
            decoded_str += str(content)
            
    return decoded_str

def clean_html(raw_html: str) -> str:
    """Strips HTML tags so ReportLab's Paragraph parser doesn't crash."""
    if not raw_html:
        return ""
  
    clean_text = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', raw_html, flags=re.DOTALL | re.IGNORECASE)
    # Strip all other HTML tags
    clean_text = re.sub(r'<[^>]+>', '', clean_text)
    
    return html.unescape(clean_text).strip()

def fetch_and_convert() -> list[dict]:
    # 1. Setup IMAP Connection
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        mail.login(os.getenv("IMAP_USER"), os.getenv("IMAP_PASS"))
    except Exception as e:
        return [{"error": f"Login failed: {str(e)}"}]
        
    mail.select("inbox")
    
    # 2. Search for Unread Emails
    _, ids = mail.search(None, "UNSEEN")
    id_list = ids[0].split()

    if not id_list:
        mail.logout()
        return [{"status": "no unread emails found"}]

    # 3. Limit to the 10 most recent unread emails
    recent_ids = id_list[-10:][::-1]
    
    print(f"DEBUG: Found {len(id_list)} unread. Processing the {len(recent_ids)} most recent.")

    results = []
    for num in recent_ids:
        try:
            print(f"DEBUG: Processing email ID {num.decode()}...")
            
            # Fetch email data
            _, data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])

            # Decode headers safely
            subject = decode_mime_header(msg.get("Subject", "No Subject"))
            sender = decode_mime_header(msg.get("From", "Unknown"))

            # 4. Extract and Clean Body Content
            raw_body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    # Prioritize plain text
                    if content_type == "text/plain":
                        raw_body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                        break
                    # Fallback to HTML if plain text isn't found
                    elif content_type == "text/html":
                        raw_body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
            else:
                raw_body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

            # Crucial: Clean HTML to prevent Paragraph ValueError
            clean_body = clean_html(raw_body)
            
            # 5. Build the PDF
            safe_subject = re.sub(r'[^\w\-]', '_', str(subject))[:40] or "email_doc"
            pdf_filename = f"{safe_subject}_{num.decode()}.pdf"
            pdf_path = os.path.join("output", pdf_filename)
            os.makedirs("output", exist_ok=True)

            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            
            # ReportLab only recognizes <br/> for line breaks within a Paragraph
            formatted_body = clean_body.replace('\n', '<br/>')

            elements = [
                Paragraph(f"<b>Subject:</b> {subject}", styles["Title"]),
                Paragraph(f"<b>From:</b> {sender}", styles["Normal"]),
                Spacer(1, 20),
                Paragraph(formatted_body or "(no text body content)", styles["Normal"]),
            ]

            doc.build(elements)
            
            # Save the buffer to file
            with open(pdf_path, "wb") as f:
                f.write(buffer.getvalue())
                
            results.append({"subject": subject, "from": sender, "saved_to": pdf_path})
            print(f"DEBUG: Successfully created {pdf_filename}")

        except Exception as e:
            error_msg = f"Failed to process email {num.decode()}: {str(e)}"
            print(f"ERROR: {error_msg}")
            results.append({"error": error_msg})

    mail.logout()
    return results