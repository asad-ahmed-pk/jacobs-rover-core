# drive_control_node.py
# Subscriber node - subscribes to /drive/cmd_vel and sends commands to RC motor
# Responsible for direct motor-control of the rover

import rospy

import RPi.GPIO as GPIO

from geometry_msgs import Twist

GPIO.setmode(GPIO.BCM)

# GPIO Pins
EngineGPIO = 4
ServoGPIO = 17

# Engine PWM values
EngineFullThrust = 12.048
EngineFullReverse = 6.024
EngineStop = 9.032

# Throttle values
EngineReverseThrottle = EngineFullReverse - EngineStop
EngineForwardThrottle = EngineFullThrust - EngineStop


def gpio_setup():
    """ GPIO setup for motor control """
    GPIO.setup(EngineGPIO, GPIO.OUT)
    GPIO.setup(ServoGPIO, GPIO.OUT)

    # engine PWM
    EnginePWM = GPIO.PWM(EngineGPIO, 60.8) # PWM Signal frequency in HZ, NOTE that Raspberry is not very accurate here!
    EnginePWM.start(0)

    # servo PWM
    ServoPWM = GPIO.PWM(ServoGPIO, 60.8) # PWM Signal frequency in HZ
    ServoPWM.start(0)


def cmd_vel_callback(data):
    """ The callback for the topic /drive/cmd_vel """
    # TODO: get thrust and turn (normalized) and call drive_motors


def drive_motors(thrust, yaw):
    """Send motor commands to drive rover

    Args:
        thrust: A unit scalar [-1.0, 1.0] where 0.0 is zero thrust (stopped) and 1.0 is full-speed forward (not recommended)
        and -1.0 is full reverse thrust (not recommended)

        yaw: A unit scalar [-1.0, 1.0] where 0.0 is no yaw (straight steering), 1.0 is a full-right turn, and -1.0 is a full left turn.

    Note: Values will be clamped to the range [-1.0, 1.0] is out of bounds
    """
    # TODO: implmement motor controller and call
