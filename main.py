from machine import Pin, reset
import json
import secrets 
from utils.led import init_leds, quick_toggle
from utils.logger import SYSTEM_LOGGER
from utils.mqtt import executeMQTTPublish
from utils.system import connect_wifi, sync_sys_time
import time

reed_pin = Pin(14, Pin.IN, Pin.PULL_UP)
last_state = -1 


try:
    init_leds()
    connect_wifi()
    sync_sys_time()

    SYSTEM_LOGGER.info("--- Shadow Publisher Running ---")
    while True:

        # Check the current state of the reed switch (0 = Closed, 1 = Open)
        current_state = reed_pin.value()
        
        # Only publish if the state has changed
        if current_state != last_state:
            status_text = "CLOSED" if current_state == 0 else "OPEN"
            SYSTEM_LOGGER.info(f"State change detected. Updating Shadow: {status_text}")
            
            # Get the current Unix timestamp
            current_time = time.time()
            quick_toggle()
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
