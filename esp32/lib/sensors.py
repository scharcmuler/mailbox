from machine import Pin, time_pulse_us
import time


class UltrasonicSensor:
    """
    Kapselt HC-SR04-ähnlichen Ultraschallsensor.
    Nutzt TRIG auf Pin 32 und ECHO auf Pin 13 (Standard).
    """

    def __init__(self, trig_pin=32, echo_pin=13, timeout_us=30000):
        self.trig = Pin(trig_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
        self.timeout_us = timeout_us

    def distance_cm(self):
        """
        Misst die Distanz in cm.
        Gibt None zurück, wenn kein Echo (Timeout oder Fehler).
        """
        # Trigger-Puls senden
        self.trig.off()
        time.sleep_us(2)
        self.trig.on()
        time.sleep_us(10)
        self.trig.off()

        # Echo-Puls messen
        duration = time_pulse_us(self.echo, 1, self.timeout_us)
        if duration < 0:
            return None

        # Umrechnung in Zentimeter (Schallgeschwindigkeit ca. 343 m/s)
        return duration / 58.0
