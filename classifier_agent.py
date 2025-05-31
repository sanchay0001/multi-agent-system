import os
from agents.email_agent import EmailAgent
from agents.json_agent import JSONAgent
from agents.pdf_agent import PDFAgent  # NEW

class ClassifierAgent:
    def __init__(self, memory):
        self.memory = memory
        self.email_agent = EmailAgent(memory)
        self.json_agent = JSONAgent(memory)
        self.pdf_agent = PDFAgent(memory)  # NEW

    def classify_format(self, filepath):
        ext = os.path.splitext(filepath)[1].lower()
        if ext == ".pdf":
            return "PDF"
        elif ext == ".json":
            return "JSON"
        elif ext in [".txt", ".eml"]:
            return "Email"
        else:
            return "Unknown"

    def classify_intent(self, filepath, format_):
        # For JSON and Email, we might have separate logic or rely on downstream agents
        # For PDF, intent detection is done inside PDFAgent.process()
        if format_ == "JSON":
            # Simple dummy intent (you can improve this)
            return "Invoice"
        elif format_ == "Email":
            # Default general for now
            return "General"
        elif format_ == "PDF":
            return None  # Handled by PDFAgent
        else:
            return "Unknown"

    def route(self, filepath):
        format_ = self.classify_format(filepath)
        intent = self.classify_intent(filepath, format_)

        print(f"[Classifier] Format: {format_}, Intent: {intent or 'N/A'}")

        if format_ == "Email":
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            self.email_agent.process(content, intent or "General", filepath)

        elif format_ == "JSON":
            import json
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.json_agent.process(data, intent or "Invoice", filepath)

        elif format_ == "PDF":
            self.pdf_agent.process(filepath, filepath)

        else:
            print("[Classifier] Unknown file format")

