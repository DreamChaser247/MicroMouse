#!/usr/bin/env python3


import RPi.GPIO as GPIO
from time import sleep

# Setup
pin = 25  # Example GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

try:
    while True:
        GPIO.output(pin, GPIO.HIGH)  # Set pin high
        sleep(3)                      # Wait for 1 second
        GPIO.output(pin, GPIO.LOW)   # Set pin low
        sleep(1)                      # Wait for 1 second
finally:
    GPIO.cleanup()  # Clean up GPIO settings
