import ssl
from umqtt.simple import MQTTClient
import secrets
from utils.logger import SYSTEM_LOGGER

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
