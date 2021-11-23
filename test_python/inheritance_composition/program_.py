
from hr_ import PayrollSystem
from employees_ import EmployeeDatabase
from productivity_ import ProductivitySystem

productivity_system = ProductivitySystem()
payroll_system = PayrollSystem()
employee_database = EmployeeDatabase()
employees = employee_database.employees
productivity_system.track(employees=employees, hours=40)
payroll_system.calculate_payroll(employees)
