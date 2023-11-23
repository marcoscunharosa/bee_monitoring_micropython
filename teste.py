from database_manager import DatabaseManager
from sensors_manager import SensorsManager
import network
import time
import socket
from do_connect import open_socket, do_connect_to_wifi
from server_manager import ServerManager
# from bme680 import BME680

database_manager = DatabaseManager()
sensors_manager = SensorsManager(database_manager)

# sensors_manager.sensors_reading()

# # # bme = BME680()
# # # bme.get_sensor_data()

ssid = 'Luverci 1744'
psk = 'semfio@1744'

try:
    print('try connect to wifi')
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, psk)

    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    
    print('Connection Success!')
    ip = wlan.ifconfig()[0]
    print(f'ip = {ip}')
except Exception as e:
    print('deu ruim', e)

connection = open_socket(ip)
server_manager = ServerManager(connection, database_manager, sensors_manager)
server_manager.listen_to_connections()
