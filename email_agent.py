 # agents/email_agent.py

import re

class EmailAgent:
    def __init__(self, memory):
        self.memory = memory

    def extract_sender(self, content):
        # Looks for typical "From: " or email patterns
        match = re.search(r"From:\s*(.*)", content, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        match = re.search(r"[\w\.-]+@[\w\.-]+", content)
        if match:
            return match.group(0)
        
        return "Unknown"

    def detect_urgency(self, content):
        if any(word in content.lower() for word in ["urgent", "asap", "immediately", "priority"]):
            return "High"
        elif "soon" in content.lower():
            return "Medium"
        else:
            return "Low"

    def process(self, content, intent, source):
        sender = self.extract_sender(content)
        urgency = self.detect_urgency(content)

        extracted = {
            "sender": sender,
            "urgency": urgency,
            "summary": content[:200]  # First 200 chars as a simple summary
        }

        print(f"[EmailAgent] Sender: {sender}, Urgency: {urgency}")
        self.memory.log(
            source=source,
            format_="Email",
            intent=intent,
            sender=sender,
            extracted_values=extracted,
            thread_id=None
        )

