from machine import Pin
from utils.led import init_leds, quick_toggle_led
from utils.logger import SYSTEM_LOGGER
from utils.mqtt import executeMQTTPublish
from utils.system import connect_wifi, sync_sys_time
import time

try:
    init_leds()
    
    quick_toggle_led(2)
    quick_toggle_led(2, "GREEN")

    connect_wifi()
  
    sync_sys_time()
    reed_pin = Pin(14, Pin.IN, Pin.PULL_DOWN)
    last_state = -1 

    SYSTEM_LOGGER.info("--- Shadow Publisher Running ---")
    while True:
        # Check the current state of the reed switch (0 = Closed, 1 = Open)
        current_state = reed_pin.value()
        
        # Only publish if the state has changed
        if current_state != last_state:
            status_text = "CLOSED" if current_state == 1 else "OPEN"
            SYSTEM_LOGGER.info(f"State change detected. Updating Shadow: {status_text}")
            
            # Get the current Unix timestamp
            current_time = time.time()
            quick_toggle_led(4, "GREEN")
            success = executeMQTTPublish({
                "state": {
                    "reported": {
                        "doorStatus": status_text,
                        "timestamp": current_time 
                    }
                }
            })
            if success:
                SYSTEM_LOGGER.info(f"Payload published. Version updated in AWS.")
            else:
                SYSTEM_LOGGER.error("Publish unsuccessful")
            
            last_state = current_state
        time.sleep(0.2)

except Exception as e:
    SYSTEM_LOGGER.fatal(f"\nFATAL ERROR: {e}.")
