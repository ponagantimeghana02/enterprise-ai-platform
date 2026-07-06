from backend.tools.base_tool import BaseTool, authenticate, authorize


class PayrollTool(BaseTool):

    def get_salary(self, user, employee_id: int):

        authenticate(user)
        authorize(user, role="admin")

        self.log("Fetching payroll data")

        return {
            "employee_id": employee_id,
            "salary": 50000
        }


payroll_tool = PayrollTool()