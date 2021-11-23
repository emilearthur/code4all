from random import randint
from datetime import datetime
from random import seed


class Robot:
    def __init__(self):
        self.name = self.generator()

    def generator(self):
        robot_name = []
        numbers = str(randint(100, 999))
        number_alpha = [randint(65, 90) for i in range(2)]

        for num in number_alpha:
            robot_name.append(chr(int(num)))

        robot_name.append(numbers)

        return ''.join(robot_name)

    def delete(self):
        self.name = None

    def reset(self):
        seed(datetime.now())
        self.delete()
        self.name = self.generator()
