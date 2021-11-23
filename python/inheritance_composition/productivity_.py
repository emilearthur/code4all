
from employees import Employee
from typing import Union, List, Dict
from dataclasses import dataclass, field


class ManagerRole:
    def perform_duties(self, hours: Union[float, int]) -> str:
        return f"screams and yells for {hours} hours."


class SecretaryRole:
    def perform_duties(self, hours: Union[float, int]) -> str:
        return f"does paper work for {hours} hours"


class SalesRole:
    def perform_duties(self, hours: Union[float, int]) -> str:
        return f"expands {hours} hours on phone."


class FactoryRole:
    def perform_duties(self, hours: Union[float, int]) -> str:
        return f"manufactures gadgets for {hours} hours."

@dataclass
class ProductivitySystem:
    _roles: Dict[str, Union[ManagerRole, SecretaryRole, SalesRole, FactoryRole]] = field(default=Dict)
    
    def __post_init__(self):
        self._roles = {
            'manager': ManagerRole,
            'secretary': SecretaryRole,
            'sales': SalesRole,
            'factory': FactoryRole,
        }

    def get_role(self, role_id: str) -> str:
        role_type = self._roles.get(role_id)
        if not role_type:
            raise ValueError('role_id')
        return role_type()

    def track(self, employees: List[Employee], hours: Union[float, int]) -> None:
        print("Tracking Employee Productivity")
        print("==============================")
        for employee in employees:
            employee.work(hours)
        print('')
