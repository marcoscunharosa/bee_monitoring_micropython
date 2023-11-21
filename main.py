#cria conexao bluetooth, cria as duas threads e chama a leitura de sensores e o server

from _thread import start_new_thread
from machine import (Pin)
from ble_listener import BleListener
from do_connect import *
from bee_server import BeeServer
from database_manager import DatabaseManager
from sensors_manager import SensorsManager

# Ativando bluetooth
ble = BleListener(do_connect_to_wifi)
ble.start_ble_loop()

# Após a conexão com o Wi-Fi, abre-se o socket do servidor
connection = open_socket(ble.connected_ip)
bee_server = BeeServer(connection)

database_manager = DatabaseManager()
sensors_manager = SensorsManager(database_manager)

start_new_thread(bee_server.listen_to_connections, ())
sensors_manager.sensors_reading()
