 # agents/json_agent.py

class JSONAgent:
    def __init__(self, memory):
        self.memory = memory

    def validate_schema(self, data, required_fields):
        missing = [field for field in required_fields if field not in data]
        return missing

    def process(self, data, intent, source):
        # Define target schema for demonstration
        target_schema = {
            "invoice_id": data.get("invoice_id"),
            "amount": data.get("amount"),
            "date": data.get("date"),
            "vendor": data.get("vendor")
        }

        missing_fields = self.validate_schema(data, ["invoice_id", "amount", "date", "vendor"])

        print(f"[JSONAgent] Processing JSON intent: {intent}")
        if missing_fields:
            print(f"[JSONAgent] ⚠️ Missing fields: {missing_fields}")
        else:
            print(f"[JSONAgent] ✅ All required fields present.")

        self.memory.log(
            source=source,
            format_="JSON",
            intent=intent,
            sender=data.get("vendor", "Unknown"),
            extracted_values=target_schema,
            thread_id=None
        )

