import math
from time import sleep
from numpy import arange
from gpiozero import AngularServo, tools


class ArmV5:

    def __init__(self, lower_length, upper_length, base_servo_pin=17, lower_servo_pin=27, upper_servo_pin=22,
                 claw_servo_pin=23):
        self.lowerLength = lower_length
        self.upperLength = upper_length
        self.totalLength = lower_length + upper_length

        self.base_servo = AngularServo(pin=base_servo_pin, min_angle=0, max_angle=180, initial_angle=90,
                                       min_pulse_width=0.5 / 1000, max_pulse_width=2.5 / 1000)
        self.lower_servo = AngularServo(pin=lower_servo_pin, min_angle=0, max_angle=180, initial_angle=90,
                                        min_pulse_width=0.5 / 1000, max_pulse_width=2.5 / 1000)
        self.upper_servo = AngularServo(pin=upper_servo_pin, min_angle=0, max_angle=180, initial_angle=90,
                                        min_pulse_width=0.5 / 1000, max_pulse_width=2.5 / 1000)

        # claw servo should NEVER go past 120 degrees
        self.claw_servo = AngularServo(pin=claw_servo_pin, min_angle=0, max_angle=180, initial_angle=120)
        sleep(1)

    def move_to_xyz(self, x, y, z):
        old_base_angle = self.base_servo.angle
        old_lower_angle = self.lower_servo.angle
        old_upper_angle = self.upper_servo.angle

        new_base_angle = self.calculate_base_angle(x, z)
        q1_q2 = self.calculate_kinematics_angles(x, y)
        new_lower_angle = q1_q2[0]
        new_upper_angle = q1_q2[1]

        delta_base_angle = new_base_angle - old_base_angle
        delta_lower_angle = new_lower_angle - old_lower_angle
        delta_upper_angle = new_upper_angle - old_upper_angle

        for i in arange(0, 1, 0.03):
            self.base_servo.angle = old_base_angle + self.QuadraticEaseInOut(i) * delta_base_angle
            self.lower_servo.angle = old_lower_angle + self.QuadraticEaseInOut(i) * delta_lower_angle
            self.upper_servo.angle = old_upper_angle + self.QuadraticEaseInOut(i) * delta_upper_angle
            sleep(0.03)

    def calculate_kinematics_angles(self, x, y):
        q2calc = (math.pow(x, 2) + math.pow(y, 2) - math.pow(self.lowerLength, 2) - math.pow(self.upperLength, 2)) / (
                2 * self.lowerLength * self.upperLength)
        if q2calc > 1:
            print("NOT IN RANGE!")
            return
        q2 = math.acos(
            q2calc)

        if x is not 0:
            q1calc = math.atan(y / x)
        else:
            q1calc = math.pi / 2

        q1 = q1calc + math.atan(
            (self.upperLength * math.sin(q2)) / (self.lowerLength + self.upperLength * math.cos(q2)))

        q2 = math.degrees(q2)
        q1 = math.degrees(q1)

        print('Q1 lower angle: ' + str(q1))
        print('Q2 upper angle: ' + str(q2))

        return [180 - q1, q2]

    def calculate_base_angle(self, x, z):
        degrees = 90
        if x != 0:
            degrees = math.degrees(math.atan(z / x)) + 90
        print('Base servo is at: ' + str(degrees) + ' degrees')
        return 180-degrees

    def calibration(self):
        self.base_servo.angle = 90
        self.lower_servo.angle = 0
        self.upper_servo.angle = 0
        self.close_claw()

    def wiggle(self, just_base=False, just_lower=False, just_upper=False):
        source_delay = 0.02
        if (just_base):
            self.base_servo.source = tools.sin_values()
            self.base_servo.source_delay = source_delay
        elif (just_lower):
            self.lower_servo.source = tools.cos_values()
            self.lower_servo.source_delay = source_delay
        elif (just_upper):
            self.upper_servo.source = tools.sin_values()
            self.upper_servo.source_delay = source_delay
        else:
            self.base_servo.source = tools.sin_values()
            self.base_servo.source_delay = source_delay
            self.lower_servo.source = tools.cos_values()
            self.lower_servo.source_delay = source_delay
            self.upper_servo.source = tools.sin_values()
            self.upper_servo.source_delay = source_delay
        sleep(20)

    def QuadraticEaseInOut(self, p):
        if (p < 0.5):
            return 2 * p * p
        return (-2 * p * p) + (4 * p) - 1

    def open_claw(self):
        self.claw_servo.angle = 0
        sleep(0.2)

    def close_claw(self):
        self.claw_servo.angle = 120
        sleep(0.2)