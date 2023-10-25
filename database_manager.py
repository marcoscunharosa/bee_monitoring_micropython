class DatabaseManager:
    def __init__(self):
        self.csv_path = 'database.csv'
        self.csv_file = open(self.csv_path, 'a')

    def get_data(self):
        csv_reader = open(self.csv_path, 'r')
        csv_lines = csv_reader.readlines()

        data = {
            "timestamps" : [],
            "proximity_readings": [],
            "external_sound_readings": [],
            "internal_sound_readings": []
        }

        for line in csv_lines[1:]:
            for data_type, reading in zip(data.keys(), line.split(',')):
                clean_reading = reading if '\n' not in reading else reading[:-2]
                data[data_type].append(clean_reading)

        return f'{str(data)}'

    def save(self, timestamp, readings):
        csv_formatted_data = self.__format_readings(timestamp, readings)
        self.csv_file.write(csv_formatted_data)
        self.csv_file.flush()

    def __format_readings(self, timestamp, readings):
        csv_formatted_readings = f'{timestamp}'
        for reading in readings:
            csv_formatted_readings += f',{reading}'
        csv_formatted_readings += '\n'

        return csv_formatted_readings

