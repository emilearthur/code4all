
from typing import Union, Dict, List
from dataclasses import dataclass, field


@dataclass
class PayrollPolicy:
    hours_worked: int = 0
    
    def track_work(self, hours: Union[float, int]):
        self.hours_worked += hours


@dataclass
class SalaryPolicy(PayrollPolicy):
    weekly_salary: Union[float, int] =  field(default=False, init=True)

    def calculate_payroll(self) -> Union[float, int]:
        return self.weekly_salary


@dataclass
class HourlyPolicy(PayrollPolicy):
    hour_rate: Union[float, int] =  field(default=False, init=True)

    def calculate_payroll(self) -> Union[float, int]:
        return self.hours_worked * self.hour_rate


@dataclass
class CommissionPolicy(SalaryPolicy):
    commission_per_sale: Union[float, int] =  field(default=False, init=True)

    @property
    def commission(self):
        sales = self.hours_worked / 5
        return sales * self.commission_per_sale

    def calculate_payroll(self) -> Union[float, int]:
        fixed = super().calculate_payroll()
        return fixed + self.commission

@dataclass
class PayrollSystem:
    _employee_policies: Dict[int, Union[SalaryPolicy, CommissionPolicy, HourlyPolicy]]  = field(default=Dict)
    
    def __post_init__(self):
        self._employee_policies = {
            1: SalaryPolicy(weekly_salary=3000),
            2: SalaryPolicy(weekly_salary=1500),
            3: CommissionPolicy(weekly_salary=1000, commission_per_sale=100),
            4: HourlyPolicy(hour_rate=15),
            5: HourlyPolicy(hour_rate=9),
        }

    def get_policy(self, employee_id:int) -> Union[float, int]:
        policy = self._employee_policies.get(employee_id)
        if not policy:
            return ValueError(employee_id)
        return policy

    def calculate_payroll(self, employees: List[dataclass]) -> None:
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
            if employee.address:
                print("- Sent to:")
                print(employee.address)
            print("")

