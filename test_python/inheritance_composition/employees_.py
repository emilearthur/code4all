
from dataclasses import dataclass, field
from typing import Union, List, Dict
from contacts import Address

from hr_ import (SalaryPolicy, CommissionPolicy, HourlyPolicy)
from productivity_ import (ManagerRole, SecretaryRole, SalesRole, FactoryRole)

from productivity_ import ProductivitySystem
from hr_ import PayrollSystem
from contacts import AddressBook


@dataclass
class Employee:
    """We making the Employee an abstract base class.  There are two side effects here;
    * You telling users of the module that objects of type Employee can't be created.
    * You telling other devs working on the hr module hat if they derive from Employee, the they must 
    override the .calculate_payroll abstract method."""
    id: int
    name: str
    role: str = field(default=False, init=True)
    payroll: str = field(default=False, init=True)
    address: Address = None

    def work(self, hours: Union[float, int]):
        duties = self.role.perform_duties(hours)
        print(f'Employee {self.id} - {self.name}:')
        print(f'- {duties}')
        print('')
        self.payroll.track_work(hours)

    def calculate_payroll(self):
        return self.payroll.calculate_payroll()
        



@dataclass
class Manager(Employee, ManagerRole, SalaryPolicy):
    id: int = field(default=False, init=False)
    name: str = field(default=False, init=False)
    weekly_salary: Union[float, int] =field(default=False, init=False)

    def __post_init__(self):
        SalaryPolicy.__init__(self, self.weekly_salary)
        super().__init__(self.id, self.name)


@dataclass
class Secretary(Employee, SecretaryRole, SalaryPolicy):
    id: int = field(default=False, init=False)
    name: str = field(default=False, init=False)
    weekly_salary: Union[float, int] = field(default=False, init=False)
    
    def __post_init__(self):
        SalaryPolicy.__init__(self, self.weekly_salary)
        super().__init__(self.id, self.name)


@dataclass
class SalesPerson(Employee, SalesRole, CommissionPolicy):
    id: int = field(default=False, init=False)
    name: str = field(default=False, init=False)
    weekly_salary: Union[float, int] = field(default=False, init=False)
    commission: int = field(default=False, init=False)

    def __post_init__(self):
        CommissionPolicy.__init__(self, self.weekly_salary, self.commission)
        super().__init__(self.id, self.name)


@dataclass
class FactoryWorker(Employee, FactoryRole, HourlyPolicy):
    id: int = field(default=False, init=False)
    name: str = field(default=False, init=False)
    hours_worked: Union[float, int] = field(default=False, init=False)
    hour_rate: Union[float, int] = field(default=False, init=False)

    def __post_init__(self):
        HourlyPolicy.__init__(self, self.hours_worked, self.hour_rate)
        super().__init__(self.id, self.name)


@dataclass
class TemporarySecretary(Employee, SecretaryRole, HourlyPolicy):
    id: int = field(default=False, init=False)
    name: str = field(default=False, init=False)
    hours_worked: Union[float, int] = field(default=False, init=False)
    hour_rate: Union[float, int] = field(default=False, init=False)

    def __post_init__(self):
        HourlyPolicy.__init__(self, self.hours_worked, self.hour_rate)
        super().__init__(self.id, self.name)


@dataclass
class EmployeeDatabase:
    _employees: List[Dict[str, str]] =  field(default=Dict)

    def __post_init__(self):
        self._employees = [
            {"id": 1, "name":"Mayr Gayns", "role": "manager"},
            {'id': 2, 'name': 'John Smith','role': 'secretary'},
            {'id': 3, 'name': 'Kevin Bacon', 'role': 'sales'},
            {'id': 4, 'name': 'Jane Doe', 'role': 'factory'},
            {'id': 5, 'name': 'Robin Williams', 'role': 'secretary'},
        ]
        self.productivity = ProductivitySystem()
        self.payroll = PayrollSystem()
        self.employee_addresses = AddressBook()

    @property
    def employees(self):
        return [self._create_employee(**data) for data in self._employees]

    def _create_employee(self, id: str, name: str, role: str):
        address = self.employee_addresses.get_employee_address(id)
        employee_role = self.productivity.get_role(role)
        payroll_policy = self.payroll.get_policy(id)
        return Employee(id=id, name=name, address=address, role=employee_role, payroll=payroll_policy)
