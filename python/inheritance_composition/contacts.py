
from dataclasses import dataclass, field
from typing import Optional, Union, Dict

@dataclass
class Address:
    street: str
    city: str
    state: str
    zipcode: str
    street2: Optional[str] = ''
    

    def __str__(self) -> str:
        """Provices pretty response of address."""
        lines = [self.street]
        if self.street2:
            lines.append(self.street2)
        lines.append(f"{self.city}, {self.state} {self.zipcode}")
        return "\n".join(lines)


@dataclass
class AddressBook:
    _employee_addresses: Dict[int, Address]= field(default=Dict)
    
    def __post_init__(self):
        self._employee_addresses = {
            1: Address('121 Admin Rd.', 'Concord', 'NH', '03301'),
            2: Address('67 Paperwork Ave', 'Manchester', 'NH', '03101'),
            3: Address('15 Rose St', 'Concord', 'NH', '03301', 'Apt. B-1'),
            4: Address('39 Sole St.', 'Concord', 'NH', '03301'),
            5: Address('99 Mountain Rd.', 'Concord', 'NH', '03301'),
            }

    def get_employee_address(self, employee_id: str) -> str:
        address = self._employee_addresses.get(employee_id)
        if not address:
            raise ValueError(employee_id)
        return address
