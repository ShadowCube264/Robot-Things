from sr.robot3 import *

robot = Robot()
arduino = robot.arduino

#Begin the spin
robot.motor_board.motors[0].power = 0.25
robot.motor_board.motors[1].power = -0.25

aligned = False

#Spin until marker of pallet found
#In general, robot keeps moving until motor power is adjusted, or code stops running
while not aligned:
    markers = robot.camera.see() #Ideally shouldn't use the camera while moving, but it's good enough for now
    for m in markers:
        if m.id == 117:
            print(m.position.horizontal_angle)
            if m.position.horizontal_angle < 0.1:
                aligned = True

#Move towards the marker
robot.motor_board.motors[1].power = 0.25

#Use ultrasound to measure distance; Camera is unreliable close to a marker
bumped = False
while not bumped:
    markers = robot.camera.see()
    distance = robot.arduino.ultrasound_measure(2, 3)
    print(distance)
    if distance < 80 and distance != 0:
            bumped = True
    if distance > 500:
        for m in markers:
            if m.id == 117:
                #Angle corrections
                if m.position.horizontal_angle < -0.1:
                    robot.motor_board.motors[0].power = -0.25
                elif m.position.horizontal_angle > 0.1:
                    robot.motor_board.motors[1].power = -0.25
                else:
                    robot.motor_board.motors[0].power = 0.25
                    robot.motor_board.motors[1].power = 0.25
                break

#Stop and pick up the pallet
robot.motor_board.motors[0].power = 0
robot.motor_board.motors[0].power = 0
robot.power_board.outputs[OUT_H0].is_enabled = True
robot.sleep(1)

#Victory spin!
robot.motor_board.motors[0].power = 1
robot.motor_board.motors[1].power = -1
robot.sleep(2)
