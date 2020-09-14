import gc
class CarModel:
    __slots__ = ['model_name','air', 'tilt', 'cruise_control', 'power_locks','alloy_wheels', 'usb_charger']

    def __init__(self, model_name, air=False, tilt=False, cruise_control=False, power_locks=False,alloy_wheels=False, usb_charger=False,):
        self.model_name = model_name 
        self.air = air 
        self.tilt = tilt
        self.cruise_control = cruise_control 
        self.power_locks = power_locks 
        self.alloy_wheels = alloy_wheels 
        self.usb_charger = usb_charger

    def check_serial(self, serial_number):
        """
        Looks up a serial number on a specific model of vechile an determines whether it has been involved in any 
        accident. 
        """
        print(f"Sorry, we are unable to check the serial number {serial_number} on the {self.model_name} at the time")


class Car:
    def __init__(self, model, color, serial):
        """
        Stores addition information as well as reference to the flyweight

        """
        self.model = model 
        self.color = color 
        self.serial = serial
    
    def check_serial(self):
        return self.model.check_serial(self.serial)