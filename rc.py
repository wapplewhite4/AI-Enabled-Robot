import robot       
from time import sleep
from evdev import InputDevice, categorize, ecodes

robot_instance = robot()

#creates object gamepad
gamepad = InputDevice('/dev/input/event1')

print('**Running**')

for event in gamepad.read_loop():

    if event.code == 1:
        if event.value >  32768:
            print('backward')
            robot_instance.backward()
        if event.value < 32768:
            print('forward')
            robot_instance.forward()
        if event.value == 32768:
            robot_instance.stop()
     
    if event.code == 3:   
        # print('right = steer')
        if event.value >  32768:
            print('right')
            robot_instance.right()
        if event.value <  32768:
            print('left')
            robot_instance.left()
        if event.value == 32768:
            robot_instance.stop()   
    if event.code == 16 or event.code == 17:
            print ('exiting')
            break
