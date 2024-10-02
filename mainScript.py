#!/usr/bin/env python3

import RPi.GPIO as GPIO
from time import sleep
import time


GPIO.setmode(GPIO.BCM)

desiredDist = 5.6 #desired distance from the right wall in centimeters
lastCheckpointDist = 0 #will be used to make new checkpoints. It will allow making a map of the maze, maybe...
sizeOfOneSquere = 25

class Motor:
    def __init__(self, firstPin, secondPin, enablePin,):
        self.firstPin = firstPin
        self.secondPin = secondPin
        self.enablePin = enablePin  
        self.currentSpeed = 0
        
        GPIO.setup(self.firstPin, GPIO.OUT)
        GPIO.setup(self.secondPin, GPIO.OUT)
        GPIO.setup(self.enablePin, GPIO.OUT)
        
        self.pwm = GPIO.PWM(enablePin, 50)
        self.pwm.start(0)
        
    def forward(self, speed):
        GPIO.output(self.firstPin, GPIO.HIGH)
        GPIO.output(self.secondPin, GPIO.LOW)
        self.pwm.ChangeDutyCycle(speed)
        self.currentSpeed = speed
            
    def backward(self, speed):
        GPIO.output(self.firstPin, GPIO.LOW)
        GPIO.output(self.secondPin, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(speed)
        self.currentSpeed = -1*speed
  
        
    def stop(self):
        self.pwm.ChangeDutyCycle(0)  
        
class Sonar:
    def __init__(self, echoPin, trigPin):
        self._echoPin = echoPin
        self._trigPin = trigPin
        self.pulseTime = 0

    def thereIsEcho(self):
        return GPIO.input(self._echoPin)
    
    def pulse(self):
        GPIO.output(self._trigPin, GPIO.HIGH)
        self.pulseTime = time.time()
        sleep(0.00001)  # 10 microseconds
        GPIO.output(self._trigPin, GPIO.LOW)
        
    
    def calculateDist(self):
        stopTime = time.time()
        elapsedTime = stopTime - self.pulseTime
        return ((elapsedTime * 34300) / 2)


sensors = [
    Sonar(6,5),
    Sonar(27, 17),
    Sonar(23, 22),
    Sonar(25, 24),
]

rightMotor = Motor(13, 19, 26)
leftMotor = Motor(16, 20, 21)

sleep(1)

distances = [0,0,0,0]

def checkpoint():
    print("make map of the walls near you")
    
try:
    while True:
        for i in sensors:
            ping = sensors[i].thereIsEcho()
            if ping:
                distances[i] = sensors[i].calculateDist()
                print(f" Sonar {i} measured {distances[i]} centimeters")
        if distances[1] < desiredDist: #assuming 1 is the front-facing sonar
            leftMotor.backward(100)
            rightMotor.forward(100)
        elif distances[0] > desiredDist: #assuming 0 is the right-facing sonar
            leftMotor.forward(100)
            rightMotor.backward(100)      
        elif distances[1] > 10: #assuming 1 is the front-facing sonar
            leftMotor.forward(100)
            rightMotor.forward(100)
            
        if distances[3] - lastCheckpointDist > sizeOfOneSquere: #assuming 3 is the rear-facing sonar
            checkpoint()
            lastCheckpointDist = distances[3]

except KeyboardInterrupt    :
    print("Keyboard interuption")
    
finally:
    GPIO.cleanup()