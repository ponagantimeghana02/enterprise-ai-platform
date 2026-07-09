from dataclasses import dataclass
from typing import List


# ----------------------------------------------------
# Cost Configuration
# ----------------------------------------------------

@dataclass
class CostMetric:
    name: str
    current_cost: float
    optimized_cost: float

    @property
    def savings(self):
        return self.current_cost - self.optimized_cost

    @property
    def savings_percent(self):
        return round((self.savings / self.current_cost) * 100, 2)


# ----------------------------------------------------
# Cost Optimizer
# ----------------------------------------------------

class CostOptimizer:

    def __init__(self):

        self.metrics: List[CostMetric] = [

            CostMetric(
                "Prompt Length",
                120,
                70
            ),

            CostMetric(
                "Token Usage",
                250,
                145
            ),

            CostMetric(
                "Embedding Generation",
                180,
                95
            ),

            CostMetric(
                "Vector Search",
                95,
                60
            ),

            CostMetric(
                "Agent Calls",
                150,
                80
            ),

            CostMetric(
                "API Requests",
                220,
                130
            )

        ]

    # ----------------------------------------------

    def total_current_cost(self):

        return sum(
            x.current_cost
            for x in self.metrics
        )

    # ----------------------------------------------

    def total_optimized_cost(self):

        return sum(
            x.optimized_cost
            for x in self.metrics
        )

    # ----------------------------------------------

    def monthly_savings(self):

        return (
            self.total_current_cost()
            -
            self.total_optimized_cost()
        )

    # ----------------------------------------------

    def yearly_savings(self):

        return self.monthly_savings() * 12

    # ----------------------------------------------

    def print_report(self):

        print("\n")
        print("=" * 95)

        print(
            f"{'Component':<25}"
            f"{'Current($)':<15}"
            f"{'Optimized($)':<18}"
            f"{'Savings($)':<15}"
            f"{'Savings %'}"
        )

        print("=" * 95)

        for item in self.metrics:

            print(

                f"{item.name:<25}"

                f"{item.current_cost:<15.2f}"

                f"{item.optimized_cost:<18.2f}"

                f"{item.savings:<15.2f}"

                f"{item.savings_percent}%"

            )

        print("=" * 95)

        print(
            f"Total Current Cost    : ${self.total_current_cost():.2f}"
        )

        print(
            f"Optimized Cost        : ${self.total_optimized_cost():.2f}"
        )

        print(
            f"Estimated Monthly Savings : ${self.monthly_savings():.2f}"
        )

        print(
            f"Estimated Yearly Savings  : ${self.yearly_savings():.2f}"
        )


# ----------------------------------------------------

if __name__ == "__main__":

    optimizer = CostOptimizer()

    optimizer.print_report()