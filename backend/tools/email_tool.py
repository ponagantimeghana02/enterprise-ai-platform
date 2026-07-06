from backend.tools.base_tool import BaseTool, authenticate


class EmailTool(BaseTool):

    def send_email(self, user, to: str, subject: str):

        authenticate(user)

        self.log(f"Sending email to {to}")

        return {
            "status": "sent",
            "to": to,
            "subject": subject
        }


email_tool = EmailTool()