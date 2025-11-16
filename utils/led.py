from machine import Pin
import time 

RED_LED = Pin(15, Pin.OUT)
ONBOARD_LED = Pin("LED", Pin.OUT)

def signal_error(is_on):
    """Turns the Red LED ON for error or OFF for clear."""
    RED_LED.value(is_on)

def signal_onboard_led(is_on):
    """Turns the on board LED ON or OFF for clear."""
    ONBOARD_LED.value(is_on)
        
def continuous_blink():
    """Takes over the CPU to signal a FATAL error."""
    while True:
        signal_error(1)
        time.sleep(0.5) 
        signal_error(0)
        time.sleep(0.5)

def quick_toggle_led(x = 4, bulb = "RED"):
    SLEEP_TIME = .1
    led, toggle_function = RED_LED, signal_error

    
    if bulb is "GREEN":
        led = ONBOARD_LED
        toggle_function = signal_onboard_led
    if bulb is "RED":
        led = RED_LED
        toggle_function = signal_error

    for i in range(x):
        val = led.value()
        toggle_function(1-val)
        time.sleep(SLEEP_TIME)
        toggle_function(1 - (1-val))
        time.sleep(SLEEP_TIME)

def init_leds():
    signal_onboard_led(0)
    signal_error(0)