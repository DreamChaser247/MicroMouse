#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

def read_distance(trig_pin, echo_pin):
    # sending pulse
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(trig_pin, GPIO.LOW)
    
    # time of the start of the pulse and time of reciving
    start_time = time.time()
    stop_time = time.time()
    

    while GPIO.input(echo_pin) == 0:
        start_time = time.time()
        

    while GPIO.input(echo_pin) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  #  speed of sound: 34300 cm/s
    return distance


GPIO.setmode(GPIO.BCM)

trigGPIO = [5, 17, 22, 24]
echoGPIO = [6, 27,23,25]

for i in range(len(trigGPIO)):    
    GPIO.setup(trigGPIO[i], GPIO.OUT)
    GPIO.setup(echoGPIO[i],  GPIO.IN)


pulse = 0  
  
time.sleep(1)
try:
    while True:
        
        print(f"\n Pulse {pulse}")
        for j in range (len(trigGPIO)):
            distance = read_distance(trigGPIO[j], echoGPIO[j])
            print(f" distance to sensor {j+1} is {distance} cm")
            time.sleep(0.1)
        pulse += 1
        time.sleep(3)
except KeyboardInterrupt:
    print("Keyboard interuption")
    
finally:
    GPIO.cleanup()