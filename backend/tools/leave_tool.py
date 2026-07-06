from backend.tools.base_tool import BaseTool, authenticate, authorize, retry


class LeaveTool(BaseTool):

    @retry()
    def apply_leave(self, user, days: int):

        authenticate(user)
        authorize(user)

        if days <= 0:
            raise Exception("Invalid leave days")

        self.log(f"{user['email']} applied for {days} days leave")

        return {
            "status": "approved",
            "days": days
        }


leave_tool = LeaveTool()