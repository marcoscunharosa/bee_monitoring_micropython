from _thread import start_new_thread
from connections_manager import ConnectionsManager
from server_manager import ServerManager
from database_manager import DatabaseManager
from sensors_manager import SensorsManager
import ujson

database_manager = DatabaseManager()
initial_device_data = database_manager.get_initial_device_json()

sensors_manager = SensorsManager(database_manager, device_data=initial_device_data)
connections_manager = ConnectionsManager(database_manager)

connection = connections_manager.connect_to_wifi()
server_manager = ServerManager(connection, database_manager, sensors_manager, connections_manager)
start_new_thread(sensors_manager.sensors_reading, ())
server_manager.listen_to_connections()
