from backend.tools.base_tool import BaseTool, authenticate


class CalendarTool(BaseTool):

    def create_event(self, user, title: str):

        authenticate(user)

        return {
            "status": "event_created",
            "title": title
        }


calendar_tool = CalendarTool()