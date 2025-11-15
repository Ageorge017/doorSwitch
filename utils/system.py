import ntptime
import time
import network
import secrets
from utils.logger import SYSTEM_LOGGER

def sync_sys_time():
    """Syncs the Pico W's internal clock using NTP."""
    SYSTEM_LOGGER.info("Synchronizing system time via NTP...")
    try:
        ntptime.host = "pool.ntp.org" 
        ntptime.settime()
        (year, month, mday, hour, minute, second, weekday, yearday) = time.localtime()
        SYSTEM_LOGGER.info(f"Time set successfully to: {year}-{month:02d}-{mday:02d} {hour:02d}:{minute:02d}:{second:02d}")
    except Exception as e:
        SYSTEM_LOGGER.error(f"NTP Time synchronization failed: {e}")
        raise


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
