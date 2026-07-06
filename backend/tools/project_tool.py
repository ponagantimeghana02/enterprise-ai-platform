from backend.tools.base_tool import BaseTool, authenticate, authorize


class ProjectTool(BaseTool):

    def get_projects(self, user):

        authenticate(user)
        authorize(user)

        return [
            {"id": 1, "name": "AI Platform"},
            {"id": 2, "name": "HR System"}
        ]


project_tool = ProjectTool()