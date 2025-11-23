from machine import Pin, time_pulse_us
import time

TRIG = Pin(32, Pin.OUT)
ECHO = Pin(13, Pin.IN)

def distance_cm():
    # Trigger-Puls senden
    TRIG.off()
    time.sleep_us(2)
    TRIG.on()
    time.sleep_us(10)
    TRIG.off()

    # Echo-Puls messen (timeout 30ms)
    duration = time_pulse_us(ECHO, 1, 30000)
    if duration < 0:
        return None

    # Umrechnung in cm
    return duration / 58.0

while True:
    d = distance_cm()
    print("dist:", d, "cm")
    time.sleep(0.5)
