import network
import time
from socket import socket
from bluetooth import BLE as bluetooth_low_energy
from lib.ble_simple_peripheral import BLESimplePeripheral

class ConnectionsManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.bluetooth = BLESimplePeripheral(bluetooth_low_energy())
        self.wifi_credentials = None
    
    def connect_to_wifi(self):
        wifi_id, password = self.get_wifi_credentials()
        ip = self.wait_for_connection(wifi_id, password)
        connection = self.open_socket(ip)

        return connection

    def get_wifi_credentials(self):
        if self.wifi_credentials:
            return self.wifi_credentials
        
        saved_credentials = self.database_manager.get_wifi_credentials()
        return saved_credentials if saved_credentials else self.get_wifi_via_bluetooth()

    def set_wifi_credentials(self, wifi_id, password):
        self.wifi_credentials = (wifi_id, password)
        self.database_manager.save_wifi_credentials(wifi_id, password)
        
    def wait_for_connection(self, wifi_id, password):
        wlan=network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(wifi_id, password)

        while wlan.isconnected() == False:
            print('Waiting for connection...')
            time.sleep(1)
        
        print('Connection Success!')
        ip = wlan.ifconfig()[0]
        return ip
    
    def open_socket(self, ip):
        print('Opening socket')

        port = 80
        connection = socket()
        connection.bind((ip, port))
        connection.listen(1)

        return connection
        
#--------------------------------------------------BlueTooth methods-------------------------------------------------------------
    
    def get_wifi_via_bluetooth(self):
        print("bluetooth listener on")
        while True:
            if self.bluetooth.is_connected():  # Check if a BLE connection is established
                self.bluetooth.on_write(self.__receive_bluetooth_message)  # Set the callback function for data reception
                print('bluetooth listener off')
                return self.wifi_credentials
    
    def __receive_bluetooth_message(self, message):
        received_string = message.decode('utf-8')
        print("received_string ", received_string)

        wifi_id, wifi_password = self.__decode_wifi_credentials(received_string)
        self.set_wifi_credentials(wifi_id, wifi_password)

    def __decode_wifi_credentials(self, string):
        _ ,wifi_id, wifi_password = string.split("|")
        return wifi_id, wifi_password

# def do_connect_to_wifi(ssid, psk):
#     print('try connect to wifi')
#     wlan=network.WLAN(network.STA_IF)
#     wlan.active(True)
#     wlan.connect(ssid, psk)

#     while wlan.isconnected() == False:
#         print('Waiting for connection...')
#         time.sleep(1)
    
#     print('Connection Success!')
#     ip = wlan.ifconfig()[0]
#     return ip

# def open_socket(ip):
#     print('Opening socket')
#     address = (ip, 80)
#     connection = socket()
#     connection.bind(address)
#     connection.listen(1)
#     return connection
