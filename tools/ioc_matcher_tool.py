from crewai.tools import BaseTool

class IOCMatcherTool(BaseTool):
    name: str = "IOCMatcherTool"
    description: str = "Matches input data against known indicators of compromise (IOCs)"

    def _run(self, anomaly_report: str):
        # Placeholder for actual IOC matching logic
        return {"matched_iocs": ["ioc1.example.com", "192.168.0.1"]}