# RoverEngine.py
# Class for controlling the rover's engine and steering

import RPi.GPIO as GPIO

class RoverEngine:

    def __init__(self):
        """ Init the engine and GPIO connections """

        # GPIO mode setup
        GPIO.setmode(GPIO.BCM)

        # GPIO pins for the engine and steering
        self.EngineGPIO = 4
        self.ServoGPIO = 17

        # Engine PWM values
        self.EngineFullThrust = 12.048
        self.EngineFullReverse = 6.024
        self.EngineStop = 9.032

        # Throttle values
        self.EngineReverseThrottle = self.EngineFullReverse - self.EngineStop
        self.EngineForwardThrottle = self.EngineFullThrust - self.EngineStop

        # setup GPIO
        self.gpio_setup()


    def gpio_setup(self):
        """ GPIO setup for motor control """
        GPIO.setup(self.EngineGPIO, GPIO.OUT)
        GPIO.setup(self.ServoGPIO, GPIO.OUT)

        # engine PWM
        self.EnginePWM = GPIO.PWM(self.EngineGPIO, 60.8) # PWM Signal frequency in HZ, NOTE that Raspberry is not very accurate here!
        self.EnginePWM.start(0)

        # servo PWM
        self.ServoPWM = GPIO.PWM(self.ServoGPIO, 60.8) # PWM Signal frequency in HZ
        self.ServoPWM.start(0)

        # intial state - stopped
        self.EnginePWM.ChangeDutyCycle(self.EngineStop)
        self.ServoPWM.ChangeDutyCycle(self.EngineStop)

    
    def shut_down(self):
        """ Clean up GPIO and shutdown engine control """
        self.EnginePWM.stop()
        GPIO.cleanup()

    
    def set_input(self, thrust, yaw):
        """ Set the given input for the engine for the given thrust and yaw """

        # apply thrust control
        if thrust >= 0.0:
            self.EnginePWM.ChangeDutyCycle(self.EngineStop + thrust * self.EngineForwardThrottle)
        else:
            self.EnginePWM.ChangeDutyCycle(self.EngineStop + thrust * self.EngineReverseThrottle)

        # apply yaw control
        if yaw >= 0.0:
            self.ServoPWM.ChangeDutyCycle(self.EngineStop + yaw * self.EngineReverseThrottle)
        else:
            self.ServoPWM.ChangeDutyCycle(self.EngineStop + yaw * self.EngineForwardThrottle)
