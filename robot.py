from board import SCL_1, SDA_1
import busio
import time

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685


class Robot():

    def __init__(self, *args, **kwargs):
        # Create the I2C bus interface.
        self.i2c_bus = busio.I2C(SCL_1, SDA_1)

        # Create a simple PCA9685 class instance.
        self.pca = PCA9685(self.i2c_bus)

        # Set the PWM frequency to 900
        self.pca.frequency = 900

        #initialize reference values for duty cycle
        self.HIGH = 0xffff
        self.MED = 0x7fff
        self.LOW = 0

        #initialize PWM pins based on ordering on PCA9685
        self.A_direction_out = [1, 2]
        self.B_direction_out = [4, 5]
        self.A_speed_out = 0
        self.B_speed_out = 6

        #initialize PWM outputs to 0
        self.pca.channels[self.A_speed_out].duty_cycle = 0
        self.pca.channels[self.A_direction_out[0]].duty_cycle = 0
        self.pca.channels[self.A_direction_out[1]].duty_cycle = 0
        self.pca.channels[self.B_direction_out[0]].duty_cycle = 0
        self.pca.channels[self.B_direction_out[1]].duty_cycle = 0
        self.pca.channels[self.B_speed_out].duty_cycle = 0
    
    #manually sets the speed of the motors
    def set_motors(self, A_speed=100, B_speed=100):
        self.set_speed(self, self.A_speed_out, A_speed)
        self.set_speed(self, self.B_speed_out, B_speed)
    
    #maps a speed value of 0-100 to a hex value which can be used to set the duty cycle
    def linear_map(speed=0):
        speed = hex((speed / 100) * 65535)
        return speed
    
    #manually sets the speed of one motor
    def set_speed(self, motor_ID=None, speed=0):
        if (motor_ID is self.A_speed_out):
            self.pca.channels[self.A_speed_out].duty_cycle = self.linear_map(speed)
        if (motor_ID is self.B_speed_out):
            self.pca.channels[self.B_speed_out].duty_cycle = self.linear_map(speed)

    def forward(self, speed=100, duration=None):
        self.set_speed(self.A_speed_out, speed)
        self.set_speed(self.B_speed_out, speed)
        self.pca.channels[self.A_direction_out[0]].duty_cycle = self.HIGH
        self.pca.channels[self.A_direction_out[1]].duty_cycle = self.LOW
        self.pca.channels[self.B_direction_out[0]].duty_cycle = self.HIGH
        self.pca.channels[self.B_direction_out[1]].duty_cycle = self.LOW

    def backward(self, speed=100, duration=None):
        self.set_speed(self.A_speed_out, speed)
        self.set_speed(self.B_speed_out, speed)
        self.pca.channels[self.A_direction_out[0]].duty_cycle = self.LOW
        self.pca.channels[self.A_direction_out[1]].duty_cycle = self.HIGH
        self.pca.channels[self.B_direction_out[0]].duty_cycle = self.LOW
        self.pca.channels[self.B_direction_out[1]].duty_cycle = self.HIGH

    def left_f(self, A_speed=100, B_speed=0, duration=None):
        self.set_speed(self.A_speed_out, A_speed)
        self.set_speed(self.B_speed_out, B_speed)
        self.pca.channels[self.A_direction_out[0]].duty_cycle = self.HIGH
        self.pca.channels[self.A_direction_out[1]].duty_cycle = self.LOW
        self.pca.channels[self.B_direction_out[0]].duty_cycle = self.LOW
        self.pca.channels[self.B_direction_out[1]].duty_cycle = self.LOW
    
    def right_f(self, A_speed=0, B_speed=100, duration=None):
        self.set_speed(self.A_speed_out, A_speed)
        self.set_speed(self.B_speed_out, B_speed)
        self.pca.channels[self.A_direction_out[0]].duty_cycle = self.LOW
        self.pca.channels[self.A_direction_out[1]].duty_cycle = self.LOW
        self.pca.channels[self.B_direction_out[0]].duty_cycle = self.HIGH
        self.pca.channels[self.B_direction_out[1]].duty_cycle = self.LOW
    
    def left_r(self, A_speed=100, B_speed=0, duration=None):
        self.set_speed(self.A_speed_out, A_speed)
        self.set_speed(self.B_speed_out, B_speed)
        self.pca.channels[self.A_direction_out[0]].duty_cycle = self.LOW
        self.pca.channels[self.A_direction_out[1]].duty_cycle = self.HIGH
        self.pca.channels[self.B_direction_out[0]].duty_cycle = self.LOW
        self.pca.channels[self.B_direction_out[1]].duty_cycle = self.LOW
    
    def right_r(self, A_speed=0, B_speed=100, duration=None):
        self.set_speed(self.A_speed_out, A_speed)
        self.set_speed(self.B_speed_out, B_speed)
        self.pca.channels[self.A_direction_out[0]].duty_cycle = self.LOW
        self.pca.channels[self.A_direction_out[1]].duty_cycle = self.LOW
        self.pca.channels[self.B_direction_out[0]].duty_cycle = self.LOW
        self.pca.channels[self.B_direction_out[1]].duty_cycle = self.HIGH
    
    def stop(self):
        self.set_speed(self.A_speed_out, 0)
        self.set_speed(self.B_speed_out, 0)
        self.pca.channels[self.A_direction_out[0]].duty_cycle = self.LOW
        self.pca.channels[self.A_direction_out[1]].duty_cycle = self.LOW
        self.pca.channels[self.B_direction_out[0]].duty_cycle = self.LOW
        self.pca.channels[self.B_direction_out[1]].duty_cycle = self.LOW