import re
import network
import time
from socket import socket
from bluetooth import BLE as bluetooth_low_energy
from lib.ble_simple_peripheral import BLESimplePeripheral

class ConnectionsManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

        self.wifi_credentials = None
        self.received_bluetooth_message = None
    
    def connect_to_wifi(self):
        ip = self.__connect_via_memory() or self.__connect_via_bluetooth()
        connection = self.open_socket(ip)

        return connection

    def __connect_via_memory(self):
        wifi_credentials = self.database_manager.get_wifi_credentials()
        if not wifi_credentials:
            return None
        
        return self.wait_for_connection(wifi_credentials)

    def wait_for_connection(self, wifi_credentials):
        try:
            name, password = wifi_credentials
            wlan=network.WLAN(network.STA_IF)
            wlan.active(True)
            wlan.connect(name, password)

            while wlan.isconnected() == False:
                print('Waiting for connection...')
                time.sleep(1)
            
            print('Connection Success!')
            ip = wlan.ifconfig()[0]
            return ip
        except Exception as e:
            print('ERRO NA CONEXAO:', e)
            return None
    
    def open_socket(self, ip):
        print('Opening socket')

        port = 80
        connection = socket()
        connection.bind((ip, port))
        connection.listen(1)

        return connection

#--------------------------------------------------BlueTooth methods-------------------------------------------------------------
    
    def __connect_via_bluetooth(self):
        self.received_bluetooth_message = ''
        self.wifi_credentials = None
        bluetooth = BLESimplePeripheral(bluetooth_low_energy())

        print('bluetooth on')
        while True:
            wifi_credentials = self.__get_wifi_credentials_via_bluetooth(bluetooth)
            ip = self.wait_for_connection(wifi_credentials)

            if ip:
                bluetooth.send(ip)
                self.database_manager.save_wifi_credentials(wifi_credentials)
                print('bluetooth off')
                return ip
            else:
                bluetooth.send('not_connected')
                self.received_bluetooth_message = ''

    def __get_wifi_credentials_via_bluetooth(self, bluetooth):
        while not self.__received_message_complete():
            if bluetooth.is_connected():
                bluetooth.on_write(self.__receive_bluetooth_message)
        
        return self.__decode_message_to_credentials()
    
    def __received_message_complete(self):
        pattern = r"\|.+?\|.+?\|"
        return bool(re.match(pattern, self.received_bluetooth_message))
    
    def __receive_bluetooth_message(self, message):
        received_string = message.decode('utf-8')
        self.received_bluetooth_message += received_string

    def __decode_message_to_credentials(self):
        _, wifi_id, wifi_password, _ = self.received_bluetooth_message.split("|")
        return (wifi_id, wifi_password)