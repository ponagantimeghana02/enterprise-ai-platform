from backend.tools.base_tool import BaseTool


class NotificationTool(BaseTool):

    def send_notification(self, message: str):

        self.log("Notification sent")

        return {
            "status": "sent",
            "message": message
        }


notification_tool = NotificationTool()