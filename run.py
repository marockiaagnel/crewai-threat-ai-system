from dotenv import load_dotenv
load_dotenv()

from crew import ThreatAICrew
from utils.kafka_producer import send_log_to_kafka

if __name__ == "__main__":
    print("🚀 Initializing Threat AI Crew...")

    email_logs = [
        "\n".join([
            "Received: from mail.example.com (203.0.113.45) by secure.domain.com",
            "Subject: Reset Your Password Immediately",
            "To: user@example.com",
            "Date: Tue, 30 Jul 2025 03:14:00 +0000",
            "Message-ID: <fakeid@attacker.com>",
            "Content: Click this link to reset your password: http://malicious.com/reset"
        ])
    ]
    for log in email_logs:
    	send_log_to_kafka(log)  # log is a string here

    print("🤖 Logs being passed to crew:", email_logs[0])
    crew_instance = ThreatAICrew()
    crew = crew_instance.get_crew(inputs={"logs": email_logs})  # ✅ Move input here
    final_output = crew.kickoff()  # ✅ No need to pass inputs again
    print("\n🎯 Final Output:\n", final_output)
