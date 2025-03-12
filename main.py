import network
import socket
import dht
import machine
import time

# WiFi Credentials
SSID = "****************"
PASSWORD = "************"

# Connect to WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

print("Connecting to WiFi...", end="")
while not wifi.isconnected():
    print(".", end="")
    time.sleep(1)

print("\nConnected! IP Address:", wifi.ifconfig()[0])

# Setup DHT11 Sensor on pin 5
sensor = dht.DHT11(machine.Pin(5))

# HTML Template for Web Page
def webpage(temp, hum):
    html = f"""
    <html>
    <head>
        <title>ESP8266/DHT11 Weather Station</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body {{ font-family: Arial; text-align: center; background-color: #f4f4f4; }}
            h1 {{ color: #333; }}
            p {{ font-size: 20px; }}
        </style>
    </head>
    <body>
        <h1>ESP8266/DHT11 Weather Station</h1>
        <p><strong>Temperature:</strong> {temp}°C</p>
        <p><strong>Humidity:</strong> {hum}%</p>
    </body>
    </html>
    """
    return html

# Setup Web Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(10)  # Set a 10-second timeout to avoid early disconnection
server.bind(("", 80))
server.listen(5)
print("Web server running... Open your browser and go to:", wifi.ifconfig()[0])

while True:
    try:
        conn, addr = server.accept()
        conn.settimeout(3)  # Prevent hanging connections
        request = conn.recv(1024)  # Read client request
        print("Connection from:", addr)

        # Read DHT11 Sensor safely
        try:
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()
        except OSError as e:
            temp = "Error"
            hum = "Error"
            print("DHT11 Read Failed:", e)
        
        # Send Response
        response = webpage(temp, hum)
        time.sleep(0.5)  # Short delay before sending response
        conn.sendall("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n" + response)
        conn.close()

    except OSError as e:
        print("Error:", e)

