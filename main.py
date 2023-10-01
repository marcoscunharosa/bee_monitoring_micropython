from machine import (Pin)
from ble_listener import BleListener
from do_connect import *
from bee_server import BeeServer

# Ativando bluetooth
ble = BleListener(do_connect_to_wifi)
ble.start_ble_loop()

# Após a conexão com o Wi-Fi, abre-se o socket do servidor
connection = open_socket(ble.connected_ip)
bee_server = BeeServer(connection)
bee_server.listen_to_connections()
