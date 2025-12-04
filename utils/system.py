import ntptime
import time
import network
import secrets
from utils.led import quick_toggle_led
from utils.logger import SYSTEM_LOGGER
from machine import Pin, reset

def sync_sys_time(max_attempts=5, delay_s=5):
    """Syncs the Pico W's internal clock using NTP."""
    ntptime.host = "129.6.15.28"
    for attempt in range(max_attempts):
        try:
            SYSTEM_LOGGER.info(f"Attempting time sync (Try {attempt + 1}/{max_attempts})...")
            ntptime.timeout = 5 # seconds
            ntptime.settime()
            SYSTEM_LOGGER.info("Time set successfully.")
            return
            
        except Exception as e:
            SYSTEM_LOGGER.error(f"Time sync failed: {e}")
            if attempt < max_attempts - 1:
                time.sleep(delay_s)
            else:
                SYSTEM_LOGGER.error(f"NTP Time synchronization failed: {e}")
            raise
                
    return


def connect_wifi():
    """Connects the Pico W to the local Wi-Fi network."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Check if already connected to speed up reboots
    if wlan.isconnected():
        SYSTEM_LOGGER.info(f'Wi-Fi already connected! IP: {wlan.ifconfig()[0]}')
        return wlan

    wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
    
    max_wait = 15
    SYSTEM_LOGGER.info(f"Attempting Wi-Fi connection...")
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        time.sleep(1)
        SYSTEM_LOGGER.info("Connecting...")

    if wlan.status() != 3:
        raise RuntimeError('Wi-Fi connection failed.')
    SYSTEM_LOGGER.info(f'\nWi-Fi Connected! IP:{wlan.ifconfig()[0]}')
    return wlan
