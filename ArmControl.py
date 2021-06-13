from time import sleep
from numpy import arange

from ArmV5 import ArmV5


def apples_in_basket():
    for i in range(3):
        armV5.move_to_xyz(7, 7, -8)
        armV5.open_claw()
        armV5.move_to_xyz(7, 3, 0)
        armV5.move_to_xyz(9, -3, 8)
        armV5.close_claw()
        armV5.move_to_xyz(7, 3, 0)


armV5 = ArmV5(lower_length=4.5, upper_length=5.5)
sleep(1)
apples_in_basket()
