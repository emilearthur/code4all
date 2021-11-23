from typing import List
from employees import Employee

class PayrollSystem:
    def calculate_payroll(self, employees: List[Employee]) -> None:
        """Takes a collection of employees and prints their id: str, name: str and check amount: float
        using the .calculate_payroll() method expoed on each employee object.

        Args:
            employees (List): collection of employees
        """
        print("Calculating Payroll")
        print("===================")
        for employee in employees:
            print(f"Payroll for: {employee.id} - {employee.name}")
            print(f"- Check amount: {employee.calculate_payroll()}")
            print("")


from dataclasses import dataclass
from typing import Union

@dataclass
class SalaryPolicy:
    weekly_salary: Union[float, int]

    def calculate_payroll(self) -> Union[float, int]:
        return self.weekly_salary


@dataclass
class HourlyPolicy:
    hours_worked: Union[float, int]
    hour_rate: Union[float, int]

    def calculate_payroll(self) -> Union[float, int]:
        return self.hours_worked * self.hour_rate


@dataclass
class CommissionPolicy(SalaryPolicy):
    commission: int

    def calculate_payroll(self) -> Union[float, int]:
        fixed = super().calculate_payroll()
        return fixed + self.commission
