from typing import List, Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import re

class LogParserInputSchema(BaseModel):
    logs: List[str] = Field(..., description="List of email log entries")

class LogParserTool(BaseTool):
    name: str = "Log Parser Tool"
    description: str = "Parses raw email logs into structured log entries"
    args_schema: Type[BaseModel] = LogParserInputSchema

    def _run(self, logs: List[str]) -> List[dict]:
        print("\n🔎 Incoming Logs to LogParserTool:\n", logs)
        parsed_logs = []

        for log in logs:
            ip_match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', log)
            ip = ip_match.group(0) if ip_match else "unknown"

            subject_match = re.search(r'Subject:\s*(.*)', log)
            subject = subject_match.group(1).strip() if subject_match else "unknown"

            link_match = re.search(r'(http[s]?://[^\s]+)', log)
            ioc = [link_match.group(1)] if link_match else []

            parsed_logs.append({
                "source": "email_log",
                "ip": ip,
                "subject": subject,
                "ioc": ioc
            })

        return parsed_logs