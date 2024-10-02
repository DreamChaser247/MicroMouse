#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

def read_distance(trig_pin, echo_pin):
    # Wysyłanie sygnału
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)  # 10 mikrosekund
    GPIO.output(trig_pin, GPIO.LOW)

    print("aaa")
    
    # Czas startu i zakończenia
    start_time = time.time()
    stop_time = time.time()
    
    print("bbb")

    while GPIO.input(echo_pin) == 0:
        start_time = time.time()
        
    print("rtrr")

    while GPIO.input(echo_pin) == 1:
        stop_time = time.time()

    print("ccc")
    # Obliczanie odległości
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Prędkość dźwięku: 34300 cm/s
    return distance

# Ustawienia GPIO
GPIO.setmode(GPIO.BCM)

# Definicje pinów dla czujników
sonars = [
    {"trig": 5, "echo": 6},  # Czwarty czujnik
    {"trig": 17, "echo": 27},
    {"trig": 24, "echo": 25},
    {"trig": 22, "echo": 23},
]

# Inicjalizacja pinów
for asd in sonars:
    GPIO.setup(asd["trig"], GPIO.OUT)
    GPIO.setup(asd["echo"], GPIO.IN)

try:
    while True:
        for i, sensor in enumerate(sonars):
            print("ciagle zyje")
            distance = read_distance(22, 23)
            print(f"AAAOdległość z czujnika {i + 1}: {distance:.2f} cm")
            print(f"{sensor['trig']}, trig ; {sensor['echo']}, echo")
            distance = read_distance(sensor["trig"], sensor["echo"])
            print("almoast")
            print(f"Odległość z czujnika {i + 1}: {distance:.2f} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("Program przerwany")

finally:
    GPIO.cleanup()
