##3-Axis Robotic Arm I built for an internship

This robotic arm was assembled from a pre-made kit, and then upgraded with metal gear servos. I initially chose an Arduino Uno as the control system, due to their low cost and ease of use. However, I wasn't able to achieve smooth servo movements with the arduino, so I swapped to a more powerful RaspberryPi. This had the added benefit of allowing me to update the control software wirelessly via SSH.

Between the first Arduino and final RaspberryPi revision of the robotic arm, I rewrote the control software 5 times. When I'd get stuck or feel unhappy with how the software was coming out, I tore much of it down and rebuilt it with my new knowledge. In its final revision, the arm featured servo easing, inverse kinematics, and path planning.

The purpose of building a robotic arm from scratch like this was twofold: investigate the posibility of desgining a low-cost educational robotic arm kit, and demonstrate robotics development for youth outreach and education. During the time I was developing the arm, I also taught robotics to elementary and middle school students aged 8-18. In class, I'd share my progress and roadblocks with the students.

![image](https://github.com/user-attachments/assets/db13909c-e69d-4595-b003-896c85670fd3)
