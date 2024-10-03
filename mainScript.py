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
        self.pulseOngoing = 0
        
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
        self.echoPin = echoPin
        self.trigPin = trigPin
        self.pulseTime = 0
        self.waitingForPulse = 0
        
                # Setup GPIO pins
        GPIO.setup(self.echoPin, GPIO.IN)
        GPIO.setup(self.trigPin, GPIO.OUT)

    def thereIsEcho(self):
        return GPIO.input(self.echoPin)
    
    def pulseOn(self):
        GPIO.output(self.trigPin, GPIO.HIGH)
        self.pulseTime = time.time()
        self.pulseOngoing =  1
        self.waitingForPulse = 1
        
        # sleep(0.00001)  # 10 microseconds
        # GPIO.output(self._trigPin, GPIO.LOW)
    def pulseOff(self):
        GPIO.output(self.trigPin, GPIO.LOW)
        self.pulseOngoing =  0
        
    
    def calculateDist(self):
        stopTime = time.time()
        # print(f"pulseTime var = {self.pulseTime}, stopTime var = {stopTime}")
        elapsedTime = stopTime - self.pulseTime
        return ((elapsedTime * 34300) / 2)


sensors = []
sensors.append(Sonar(6,5))
sensors.append(Sonar(27, 17))
sensors.append(Sonar(23, 22))
sensors.append(Sonar(25, 24))

rightMotor = Motor(13, 19, 26)
leftMotor = Motor(16, 20, 21)

sleep(1)

distances = [0,0,0,0]

lastPulseTick = time.time() - 3

def checkpoint():
    print("make map of the walls near you")
    
def pulseOperations(tick):
    global lastPulseTick  # Declare `lastPulseTick` as global to update it
    if tick - lastPulseTick >= 3:
        for i, sensor in enumerate(sensors):
            sensor.pulseOn()
            print("pulse was sent")
            lastPulseTick = time.time()
            
    for i, sensor in enumerate(sensors):
        if sensor.pulseTime - tick > 0.00005 and sensor.pulseOngoing:
            sensor.pulseOff()

    
try:
    while True:
        tick = time.time()
        
        for idx, sensor in enumerate(sensors):
            ping = sensor.thereIsEcho()  # Use `sensor` directly instead of `sensors[i]`
            if ping and sensor.waitingForPulse:
                distances[idx] = sensor.calculateDist()  # Use `sensor` for measurements
                print(f" Sonar {idx} measured {distances[idx]} centimeters")
                
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
            
        pulseOperations(tick)
            
        # print(f"time is {time.time()}")

except KeyboardInterrupt    :
    print("Keyboard interuption")
    
finally:
    GPIO.cleanup()