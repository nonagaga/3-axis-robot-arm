from ArmV5 import ArmV5

# servos blew up, trying to see if they still work (they didn't)

arm = ArmV5(lower_length=4.5, upper_length=5.5)

while(True):
    arm.claw_servo.angle = int(input("Enter a upper arm servo position (0-180)"))