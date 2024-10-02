#!/usr/bin/env python3

import RPi.GPIO as GPIO
from time import sleep

in1 = 13 
in2 = 19
enA = 26

in3 = 16
in4 = 20
enB = 21

GPIO.setmode(GPIO.BCM)


GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(enA, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)   
GPIO.setup(enB, GPIO.OUT)


pwmA = GPIO.PWM(enA, 50)
pwmA.start(0)

pwmB = GPIO.PWM(enB, 50)
pwmB.start(0)


def turnRight(speed: int):
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    pwmA.ChangeDutyCycle(speed)
    
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    pwmB.ChangeDutyCycle(speed)
    print("turn right")

def turnLeft(speed: int):
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    pwmA.ChangeDutyCycle(speed)
    
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    pwmB.ChangeDutyCycle(speed)
    print("turn left")

def goForward(speed: int):
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    pwmA.ChangeDutyCycle(speed)
    
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    pwmB.ChangeDutyCycle(speed)
    print("go forward")
    
def goBackward(speed):
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    pwmA.ChangeDutyCycle(speed)
    
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    pwmB.ChangeDutyCycle(speed)
    print("go forward")

def stop():
    pwmB.ChangeDutyCycle(0)
    pwmA.ChangeDutyCycle(0)
    
    
def checkpoint():
    print("make map of the walls near you")
    
desiredDist = 5.6 #desired distance from the right wall in centimeters
lastCheckpointDist = 0 #will be used to make new checkpoints. It will allow making a map of the maze, maybe...
sizeOfOneSquere = 25


def decidionPoint(frontDist: int, rightDist: int, leftDist: int, rearDist: int):
   
    if (rightDist > desiredDist):
        turnRight(100) 
    elif (frontDist < 10):
        turnLeft(100)
        
    if (frontDist >= 10):
        goForward(100)
        
    if (rearDist - lastCheckpointDist > sizeOfOneSquere):
        checkpoint()
        lastCheckpointDist = rearDist
            

# Test the functions
try:
    goForward(100)
    sleep(2)  # Use shorter sleep for testing
    turnLeft(100)
    sleep(2)
    turnRight(100)
    sleep(2)
finally:
    stop()
    GPIO.cleanup()  # Cleanup GPIO pins

