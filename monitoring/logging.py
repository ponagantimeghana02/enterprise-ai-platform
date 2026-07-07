import json
import logging
import smtplib
import requests
from datetime import datetime
from email.mime.text import MIMEText



logger = logging.getLogger("enterprise")

logger.setLevel(logging.INFO)

handler = logging.StreamHandler()

# JSON Formatter
class JsonFormatter(logging.Formatter):

    def format(self, record):

        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }

        return json.dumps(log)

handler.setFormatter(JsonFormatter())

logger.addHandler(handler)



SLACK_WEBHOOK = "https://hooks.slack.com/services/YOUR/WEBHOOK"

EMAIL_FROM = "alerts@example.com"
EMAIL_TO = "admin@example.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your_email@gmail.com"
SMTP_PASSWORD = "your_password"

#

def send_slack_alert(message: str):

    try:
        requests.post(
            SLACK_WEBHOOK,
            json={"text": message},
            timeout=5,
        )
    except Exception as e:
        logger.error(f"Slack Alert Failed: {e}")


def send_email_alert(subject: str, message: str):

    try:

        msg = MIMEText(message)

        msg["Subject"] = subject
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        server.starttls()

        server.login(
            SMTP_USERNAME,
            SMTP_PASSWORD,
        )

        server.sendmail(
            EMAIL_FROM,
            EMAIL_TO,
            msg.as_string(),
        )

        server.quit()

    except Exception as e:
        logger.error(f"Email Alert Failed: {e}")


def send_grafana_alert(message: str):

    logger.warning(f"[Grafana Alert] {message}")


def high_error_rate(rate: float):

    message = f"High Error Rate Detected : {rate}%"

    logger.error(message)

    send_slack_alert(message)

    send_email_alert("High Error Rate", message)

    send_grafana_alert(message)


def slow_response(response_time: float):

    message = f"Slow Response : {response_time:.2f} sec"

    logger.warning(message)

    send_slack_alert(message)

    send_email_alert("Slow Response", message)

    send_grafana_alert(message)


def high_cpu(cpu: float):

    message = f"High CPU Usage : {cpu}%"

    logger.warning(message)

    send_slack_alert(message)

    send_email_alert("High CPU", message)

    send_grafana_alert(message)


def high_memory(memory: float):

    message = f"High Memory Usage : {memory}%"

    logger.warning(message)

    send_slack_alert(message)

    send_email_alert("High Memory", message)

    send_grafana_alert(message)


def failed_agent(agent_name: str):

    message = f"Agent Failed : {agent_name}"

    logger.error(message)

    send_slack_alert(message)

    send_email_alert("Agent Failure", message)

    send_grafana_alert(message)


def failed_workflow(workflow_name: str):

    message = f"Workflow Failed : {workflow_name}"

    logger.error(message)

    send_slack_alert(message)

    send_email_alert("Workflow Failure", message)

    send_grafana_alert(message)



def log_info(message: str):

    logger.info(message)


def log_warning(message: str):

    logger.warning(message)


def log_error(message: str):

    logger.error(message)