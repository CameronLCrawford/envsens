import adafruit_dht
from time import sleep

class DHT22:
    TIMEOUT_LIMIT = 10

    def __init__(self, pin):
        self.name = "DHT22"
        self.device = adafruit_dht.DHT22(pin, use_pulseio=False)

    def poll(self):
        attempts = DHT22.TIMEOUT_LIMIT
        while attempts > 0:
            try:
                temp = self.device.temperature
                hum = self.device.humidity
                break
            except RuntimeError:
                attempts -= 1
                sleep(1)
                continue
            except Exception:
                return
        if attempts == 0:
            return -1
        return {"temp": temp, "hum": hum}
