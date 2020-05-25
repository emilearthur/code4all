class Shirt:
    
    def __init__(self, shirt_color, shirt_size, shirt_style, shirt_price):
        self._price = shirt_price

    def get_price(self):
        return self._price
    
    def set_price(self, new_price):
        self._price = new_price


class Pants():
    """The Pants class represents an artilce of clothing sold in a shop
    """
    def __init__(self, color, waist_size, length, price):
        """Method for initializing a Pant object 
        Args:
            color(str)
            waist_size(int)
            length(int) 
            price(float) 
        Attributes:
            color(str): color of a pants object 
            waist_size(str): waist size of a pants object
            length(str): length of a pants object
            price(float): price of a pants object
        """
        self.color = color 
        self.waist_size = waist_size
        self.length = length 
        self.price = price 

    def change_price(self, new_price):
        """The change_price method changes the price attributes of the pants object 
        Args:
            new_price(float): the new price of the pants object 
        Returns: None
        """
        self.price = new_price
    
    def discount(self, percentage):
        """The discount method outputs a discounted price of a pant object 
        Args:
            percentage(float): a decimal representing the amount to discount
        Returns: 
            float: the discounted price
        """
        return self.price * (1 - percentage)

# test script 
def check_results():
    pants = Pants('red', 35, 36, 15.12)
    assert pants.color == 'red'
    assert pants.waist_size == 35
    assert pants.length == 36
    assert pants.price == 15.12
    
    pants.change_price(10) == 10
    assert pants.price == 10 
    
    assert pants.discount(.1) == 9
    
    print('You made it to the end of the check. Nice job!')

check_results()


class SalesPerson():
    """The SalesPerson class reperesents an employee in the store
    """
    def __init__(self, first_name, last_name, employee_id, salary):
        """Method for initailization a SalesPerson object
        Args:
            first_name(str) 
            last_name(str)
            employee_id(int)
            salary(float)
        Attributes: 
            first_name (str): first name of the employee 
            last_name (str): last name of the employee
            employee_id (int): identification number of the employee 
            salary (float): yearly salary of the employee 
            pants_sold (list): a list of pants object sold by the employees 
            total_sales (float): sum of all sales made by the employees

        """
        self.first_name = first_name 
        self.last_name = last_name
        self.employee_id = employee_id
        self.salary = salary
        self.pants_sold = []
        self.total_sales = 0
        

    def sell_pant(self,pant_object):
        """The sell_pants method appends a pants object to the pants sold attributes

        Args:
            pant_object (obj): a pants object that was sold 

        Returns: None
        """
        self.pants_sold.append(pant_object)

    def display_sales(self):
        """The display_sales method prints out all pants sold 
        Args: None 

        Returns: None
        """
        for pants in self.pants_sold:
            print("color: {}, waist_size: {}, length: {}, price: {}"\
                .format(pants.color, pants.waist_size, pants.length, pants.price))
    
    def calculate_sales(self):
        """The calculate_sales method sum the total price of all pants sold 
        Args: None 

        Returns:
            float: sum of the price for all pants sold 
        """
        total = 0 
        for pants in pants_sold:
            total += pants.price

        self.total_sales = total

    

    def calculate_commission(self,percentage):
        """The calculate_commission method outputs the commission based on the percentage

        Args:
            percentage (float): the commission percentage as a decimal 

        Returns:
            float: the commissio due
        """
        sales_total = self.calculate_sales()
        return  sales_total*percentage

