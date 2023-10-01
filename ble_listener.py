from ble_simple_peripheral import BLESimplePeripheral
import bluetooth
import re

class BleListener:
    def __init__(self, connect_in_internet):
        # Inicializando a variável que salva as credenciais do Wi-Fi
        # Create a Bluetooth Low Energy (BLE) object
        ble = bluetooth.BLE()
        # Create an instance of the BLESimplePeripheral class with the BLE object
        sp = BLESimplePeripheral(ble)
        self.wi_fi_credentials = ''
        self.sp = sp
        self.is_bluetooth_on = True
        self.connect_in_internet = connect_in_internet
        self.connected_ip = None


    ####### WiFi ########
    # Função que fará a conexão do Wi-Fi
    def __try_connect_to_Wifi(self, ssid, password):
        try:
            ip = self.connect_in_internet(ssid, password)
            return ip
        except:
            return None

    # Pega credenciais do Wi-Fi de acordo com a mensagem vinda do bluetooth
    def __get_Wifi_information_from_bluetooth(self, received_string):
        # Divida a string usando "|" como delimitador para obter partes
        parts = received_string.split('|')

        ssid = parts[1]
        password = parts[2]

        return ssid, password

    ###### Bluetooth ######

    # Verifica se as credenciais estão no padrão correto |ssid|password|
    def __is_valid_credentials(self):
        pattern = r"^\|(\w+)\|(\w+)\|$"
        return re.match(pattern, self.wi_fi_credentials)

    # Define a callback to para lidar com os dados recebidos
    def __on_rx(self, data):
        print(data)
        received_string = data.decode('utf-8')
        print("received_string ", received_string)
        self.wi_fi_credentials += received_string
        if self.__is_valid_credentials() is not None:
            self.__connect_in_internet()
        elif received_string == "disconnect":
            self.is_bluetooth_on = False
                
    def __connect_in_internet(self):
        ssid, password = self.__get_Wifi_information_from_bluetooth(self.wi_fi_credentials)
        self.connected_ip = self.__try_connect_to_Wifi(ssid, password)
        if self.connected_ip is not None:
            print("sending ip")
            self.sp.send(self.connected_ip)
        else:
            self.sp.send("not_connected")

    def start_ble_loop(self):
        print("bluetooth listener on")
        while self.is_bluetooth_on:
            if self.sp.is_connected():  # Check if a BLE connection is established
                self.sp.on_write(self.__on_rx)  # Set the callback function for data reception


