# Extending built-in function 

class SillyInt(int):
    def __add__(self, num):
        return 0 
        