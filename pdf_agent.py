# agents/pdf_agent.py

import PyPDF2

class PDFAgent:
    def __init__(self, memory):
        self.memory = memory

    def extract_text(self, filepath):
        text = ""
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    def detect_intent(self, text):
        lowered = text.lower()
        if "invoice" in lowered:
            return "Invoice"
        elif "complaint" in lowered:
            return "Complaint"
        elif "request for quote" in lowered or "rfq" in lowered:
            return "RFQ"
        elif "regulation" in lowered:
            return "Regulation"
        else:
            return "General"

    def process(self, filepath, source):
        text = self.extract_text(filepath)
        intent = self.detect_intent(text)
        summary = text[:200]

        print(f"[PDFAgent] Detected intent: {intent}")
        self.memory.log(
            source=source,
            format_="PDF",
            intent=intent,
            sender="Unknown",
            extracted_values={"summary": summary},
            thread_id=None
        )
