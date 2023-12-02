import ujson
import machine
from lib.sdcard import SDCard
import uos
from utils import file_exists

class DatabaseManager:
    def __init__(self):
        self.database_path = '/sd/database.csv'
        self.device_path = '/sd/device.txt'
        self.wifi_credentials_path = '/sd/wifi_credentials.txt'
        self.data_order = [
            "timestamps",
            "proximity",
            "external_sound",
            "internal_sound"
        ]

        self.__set_microSD()
        self.database = self.__set_database()
    
#-------------------------------------------------------readers---------------------------------------------------------

    def get_file_data(self, path):
        file = open(path, 'r')
        data = file.read()
        file.close()

        return data

    def get_device_data(self):
        return self.get_file_data(self.device_path)
    
    def get_wifi_credentials(self):
        if not file_exists(self.wifi_credentials_path):
            return None
        
        data = self.get_file_data(self.wifi_credentials_path)
        return data.split(',')    

    def get_readings(self, timestamp_lower_bound, timestamp_upper_bound):
        database_reader = self.__get_database_reader()
        readings_dict = {reading_type: [] for reading_type in self.data_order}

        while True:
            entry = database_reader.readline()
            if not entry:
                break
            elif entry[-1] == '\n':
                entry = entry[:-2]

            readings = entry.split(',')
            if int(readings[0]) < timestamp_lower_bound:
                continue
            elif int(readings[0]) > timestamp_upper_bound:
                break

            for reading_type, reading in zip(readings_dict, readings):
                readings_dict[reading_type].append(reading)

        return ujson.dumps(readings_dict)

#-------------------------------------------------------writers---------------------------------------------------------

    def save_data(self, path, data):
        file = open(path, 'w')
        file.write(data)
        file.close()
    
    def save_device(self, device_data):
        self.save_data(self.device_path, device_data)
    
    def save_wifi_credentials(self, wifi_credentials):
        name, password = wifi_credentials
        self.save_data(self.wifi_credentials_path, f'{name},{password}')

    def save_readings(self, timestamp, readings):
        csv_formatted_data = self.__format_readings(timestamp, readings)

        self.database.write(csv_formatted_data)
        self.database.flush()

#-------------------------------------------------------erasers---------------------------------------------------------

    def clear(self):
        uos.remove(self.database_path)
        self.database = self.__set_database()
    
    def erase_wifi_credentials(self):
        uos.remove(self.wifi_credentials_path)

    def erase_device_data(self):
        uos.remove(self.device_path)

#-------------------------------------------------------settings---------------------------------------------------------

    def __format_readings(self, timestamp, readings):
        csv_formatted_readings = f'{timestamp}'

        for reading_type in self.data_order[1:]:
            csv_formatted_readings += f',{readings[reading_type]}'

        return csv_formatted_readings + '\n'
    
    def __set_microSD(self):
        cs = machine.Pin(9, machine.Pin.OUT)
        spi = machine.SPI(1,
                        baudrate=1000000,
                        polarity=0,
                        phase=0,
                        bits=8,
                        firstbit=machine.SPI.MSB,
                        sck=machine.Pin(10),
                        mosi=machine.Pin(11),
                        miso=machine.Pin(8))

        sd = SDCard(spi, cs)

        vfs = uos.VfsFat(sd)
        uos.mount(vfs, "/sd")
    
    def __set_database(self):
        header = ','.join(self.data_order) + '\n'

        if file_exists(self.database_path):
            database = open(self.database_path, 'a')
        else:
            database = open(self.database_path, 'a')
            database.write(header)
            database.flush()

        return database
    
    def __get_database_reader(self):
        database_reader = open(self.database_path, 'r')
        _ = database_reader.readline()

        return database_reader