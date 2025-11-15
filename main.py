from machine import Pin, reset
import json
import secrets 
from utils.logger import SYSTEM_LOGGER
from utils.system import connect_wifi, sync_sys_time
from utils.mqtt import get_mqtt_client
import time

reed_pin = Pin(14, Pin.IN, Pin.PULL_UP)
last_state = -1 


try:
    connect_wifi()
    sync_sys_time()
    client = get_mqtt_client()
    
    if client:
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
                
                # Construct the Device Shadow JSON payload
                payload = json.dumps({
                    "state": {
                        "reported": {
                            "doorStatus": status_text,
                            "timestamp": current_time 
                        }
                    }
                })
                
                # Publish the message to the reserved Shadow update topic
                client.publish(secrets.MQTT_TOPIC, payload.encode('utf-8'))
                SYSTEM_LOGGER.info(f"Payload published. Version updated in AWS.")
                
                last_state = current_state

            # Must call check_msg periodically to maintain connection keepalive
            client.check_msg() 
            time.sleep(0.2)
    else:
        raise ValueError("No Client")

except Exception as e:
    SYSTEM_LOGGER.fatal(f"\nFATAL ERROR: {e}.")
