import machine
import sdcard
import uos
from utils import file_exists

class DatabaseManager:
    def __init__(self):
        self.database_path = '/sd/database.csv'
        self.device_path = '/sd/device.txt'
        self.database_reading_positions = {
            "timestamps" : 0,
            "proximity": 1,
            "external_sound": 2,
            "internal_sound": 3,
        }

        self.__set_microSD()
        self.database = self.__set_database()

    def get_data(self, timestamp_lower_bound):
        database_reader = self.get_database_reader()
        readings_dict = {reading_type: [] for reading_type in self.database_reading_positions}

        while True:
            entry = database_reader.readline()
            if not entry:
                break
            elif entry[-1] == '\n':
                entry = entry[:-2]

            readings = entry.split(',')
            if int(readings[0]) < timestamp_lower_bound:
                continue

            for reading_type in readings_dict:
                position = self.database_reading_positions[reading_type]
                readings_dict[reading_type].append(readings[position])

        return str(readings_dict)

    def save(self, timestamp, readings):
        csv_formatted_data = self.__format_readings(timestamp, readings)

        self.database.write(csv_formatted_data)
        self.database.flush()
    
    def clear(self):
        _ = open(self.database_path, 'w').close()
        self.database = self.__set_database()
    
    def save_device(self, device_data):
        file = open(self.device_path, 'w')
        file.write(device_data)
        file.close()

    def get_device_data(self):
        file = open(self.device_path, 'r')
        data = file.read()
        file.close()

        return data

    def __format_readings(self, timestamp, readings):
        csv_formatted_readings = f'{timestamp}'

        for reading in readings:
            csv_formatted_readings += f',{reading}'

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

        sd = sdcard.SDCard(spi, cs)

        vfs = uos.VfsFat(sd)
        uos.mount(vfs, "/sd")
    
    def __set_database(self):
        database_header = 'timestamps,proximity,internal_sound,external_sound\n'

        if file_exists(self.database_path):
            database = open(self.database_path, 'a')
        else:
            database = open(self.database_path, 'a')
            database.write(database_header)
            database.flush()

        return database
    
    def get_database_reader(self):
        database_reader = open(self.database_path, 'r')
        _ = database_reader.readline()

        return database_reader