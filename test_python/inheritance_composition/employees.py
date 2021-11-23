### Abstract base classes exists to be inherited but never instancited. 
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Union


@dataclass
class Employee(ABC):
    """We making the Employee an abstract base class.  There are two side effects here;
    * You telling users of the module that objects of type Employee can't be created.
    * You telling other devs working on the hr module hat if they derive from Employee, the they must 
    override the .calculate_payroll abstract method."""
    id: int
    name: str

    @abstractmethod
    def calculate_payroll(self):
        pass


@dataclass
class SalaryEmployee(Employee):
    """Salary Employee Inherits Employee base class and add weekly_salary data.
    """
    weekly_salary: Union[float, int]

    def calculate_payroll(self) -> Union[float, int]:
        """Calulate the payroll and returns pay.
        """
        return self.weekly_salary


@dataclass
class HourlyEmployee(Employee):
    """Hourly Employee Inherits Employee base class and add hours_worked and hour_rate data.
    """
    hours_worked: Union[float, int]
    hour_rate: Union[float, int]

    def calculate_payroll(self) -> Union[float, int]:
        """Calulate the payroll and returns pay.
        """
        return self.hours_worked * self.hour_rate


@dataclass
class CommissionEmployee(SalaryEmployee):
    """Comission Employee Inherits SalaryEmployee base class and add commission data.
    """
    commission: int

    def calculate_payroll(self) -> Union[float, int]:
        """Calulate the payroll from SalaryEmployee class using super() and adds commisssion.
        """
        fixed = super().calculate_payroll()
        return fixed + self.commission



class Manager(SalaryEmployee):
    def work(self, hours: Union[float, int]) -> str:
        print(f"{self.name} screams and yells for {hours} hours")

class Secretary(SalaryEmployee):
    def work(self, hours: Union[float, int]) -> str:
        print(f"{self.name} expands {hours} hours doing office paperwork")


class SalesPerson(CommissionEmployee):
    def work(self, hours: Union[float, int]) -> str:
        print(f"{self.name} expands {hours} hours on the phone")


class FactoryWorker(HourlyEmployee):
    def work(self, hours: Union[float, int]) -> str:
        print(f"{self.name} manufactures gadgets for {hours} hours")

@dataclass
class TemporarySecretary(HourlyEmployee, Secretary):
    weekly_salary: Union[float, int]
    

    def __post_init__(self):
        HourlyEmployee.__init__(self, self.id, self.name, self.hours_worked, self.hour_rate)
