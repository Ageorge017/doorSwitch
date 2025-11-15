import json
import ssl
from umqtt.simple import MQTTClient
import secrets
from utils.logger import SYSTEM_LOGGER
import time 

def get_mqtt_client():
    """Connects to AWS IoT Core using mutual TLS (certificates)."""   
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile=secrets.AMAZON_CA)
        context.load_cert_chain(secrets.CERTIFICATE_DER, secrets.PRIVATE_DER)

        mqtt_client = MQTTClient(client_id=secrets.CLIENT_ID, server=secrets.AWS_ENDPOINT, port=8883, keepalive=1200, ssl=context)
        mqtt_client.connect()
        SYSTEM_LOGGER.info("CONNECTED CLIENT")

        SYSTEM_LOGGER.info("MQTT Connected to AWS IoT!")
        return mqtt_client

    except Exception as e:
        SYSTEM_LOGGER.error(f"MQTT Connection Failed: {e}")
        return None


MQTT_CLIENT = None
RECONNECT_ATTEMPTS = 3

def executeMQTTPublish(obj) -> bool:
    global MQTT_CLIENT
    
    # 1. Ensure Client Object Exists
    if MQTT_CLIENT is None:
        SYSTEM_LOGGER.info("MQTT client is not initialized. Attempting connection.")
        MQTT_CLIENT = get_mqtt_client()
        
    payload = json.dumps(obj)
    
    for attempt in range(RECONNECT_ATTEMPTS):
        try:
            if MQTT_CLIENT:
                MQTT_CLIENT.publish(secrets.MQTT_TOPIC, payload.encode('utf-8'))
                SYSTEM_LOGGER.info(f"Published payload (Attempt {attempt + 1}).")
                return True
            
        except Exception as e:
            SYSTEM_LOGGER.error(f"Publish failed (Attempt {attempt + 1}): {e}")
            
            global MQTT_CLIENT
            MQTT_CLIENT = None 
            
            if attempt < RECONNECT_ATTEMPTS - 1:
                SYSTEM_LOGGER.info("Connection lost. Trying to reconnect...")
                time.sleep(2) 
                MQTT_CLIENT = get_mqtt_client()
                
                if MQTT_CLIENT is None:
                    SYSTEM_LOGGER.error("Reconnection failed.")
                else:
                    SYSTEM_LOGGER.info("Reconnected successfully.")
                    
            else:
                SYSTEM_LOGGER.error(f"Failed to publish after {RECONNECT_ATTEMPTS} attempts. Halting.")
                return False
    
    return False