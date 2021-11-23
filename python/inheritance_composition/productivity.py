
from employees import Employee
from typing import Union, List

class ProductivitySystem:
    def track(self, employees: List[Employee], hours: Union[float, int]) -> None:
        print("Tracking Employee Productivity")
        print("==============================")
        for employee in employees:
            result = employee.work(hours)
            print(f'{employee.name}: {result}')
        print('')

class ManagerRole:
    def work(self, hours: Union[float, int]) -> str:
        return f"screams and yells for {hours} hours."


class SecretaryRole:
    def work(self, hours: Union[float, int]) -> str:
        return f"expands {hours} hours doing office paperwork."


class SalesRole:
    def work(self, hours: Union[float, int]) -> str:
        return f"expands {hours} hours on phone."


class FactoryRole:
    def work(self, hours: Union[float, int]) -> str:
        return f"manufactures gadgets for {hours} hours."
