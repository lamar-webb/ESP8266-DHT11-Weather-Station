import dht
import machine
import time

# Setup DHT11 on pin 5
sensor = dht.DHT11(machine.Pin(5))

while True:
    try:
        sensor.measure()  # Get sensor readings
        temp = sensor.temperature()
        hum = sensor.humidity()
        print(f"Temperature: {temp}°C, Humidity: {hum}%")
    except OSError as e:
        print("DHT11 Read Failed:", e)

    time.sleep(2)  # Wait 2 seconds before next reading

