from machine import Pin
import time 

RED_LED = Pin(15, Pin.OUT)

def signal_error(is_on):
    """Turns the Red LED ON for error or OFF for clear."""
    RED_LED.value(is_on)

def continuous_blink():
    """Takes over the CPU to signal a FATAL error."""
    while True:
        RED_LED.value(1)
        time.sleep(0.5) 
        RED_LED.value(0)
        time.sleep(0.5)