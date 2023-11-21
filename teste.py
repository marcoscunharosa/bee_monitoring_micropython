from database_manager import DatabaseManager
from sensors_manager import SensorsManager
import network
import time
import socket
from do_connect import open_socket, do_connect_to_wifi
from bee_server import BeeServer
# from bme680 import BME680

# database_manager = DatabaseManager()
# sensors_manager = SensorsManager(database_manager)

# sensors_manager.sensors_reading()

# bme = BME680()
# bme.get_sensor_data()

# ssid = 'Luverci 1744'
# psk = 'semfio@1744'
# try:
#     print('try connect to wifi')
#     wlan=network.WLAN(network.STA_IF)
#     wlan.active(True)
#     wlan.connect(ssid, psk)

#     while wlan.isconnected() == False:
#         print('Waiting for connection...')
#         time.sleep(1)
    
#     print('Connection Success!')
#     ip = wlan.ifconfig()[0]
#     print(f'ip = {ip}')
# except:
#     print('deu ruim')

# connection = open_socket(ip)
# bee_server = BeeServer(connection, database_manager)
# bee_server.listen_to_connections()


# --------------------------------------------------------

# database_manager.get_data()

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_bme680

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
temperature_offset = -5

while True:
    print("\nTemperature: %0.1f C" % (bme680.temperature + temperature_offset))
    print("Gas: %d ohm" % bme680.gas)
    print("Humidity: %0.1f %%" % bme680.relative_humidity)
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude = %0.2f meters" % bme680.altitude)

    time.sleep(1)