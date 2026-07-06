from backend.tools.base_tool import BaseTool, authenticate, authorize, retry


class EmployeeTool(BaseTool):

    @retry(max_retries=3)
    def get_employee(self, user, employee_id: int):

        # AUTH
        authenticate(user)
        authorize(user, role="admin")

        # VALIDATION
        if employee_id <= 0:
            raise Exception("Invalid employee ID")

        # LOGGING
        self.log(f"Fetching employee {employee_id}")

        # MOCK RESPONSE (replace DB later)
        return {
            "id": employee_id,
            "name": "John Doe",
            "department": "Engineering"
        }


employee_tool = EmployeeTool()