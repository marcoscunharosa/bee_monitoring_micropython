import network
import time
import socket
from server_manager import ServerManager
from database_manager import DatabaseManager
from sensors_manager import SensorsManager
from connections_manager import ConnectionsManager

# from bme680 import BME680
database_manager = DatabaseManager()
database_manager.__set_microSD()
