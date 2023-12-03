import machine
from time import sleep, localtime, time
class SensorsManager:
    def __init__(self, database_manager, device_data=None) -> None:
        # bme680 = self.__set_bme680()
        self.sensors = {
            'proximity': {'object': self.__set_proximity_sensor(), 'read_method': self.__read_proximity},
            'internal_sound': {'object': self.__set_internal_sound_sensor(), 'read_method': self.__read_internal_sound},
            'external_sound': {'object': self.__set_external_sound_sensor(), 'read_method': self.__read_external_sound},
            # 'temperature': {'object': bme680, 'read_method': self.__read_temperature},
            # 'pressure': {'object': bme680, 'read_method': self.__read_pressure},
            # 'humidity': {'object': bme680, 'read_method': self.__read_humidity}
        }

        self.database_manager = database_manager
        self.timer = self.set_timer(device_data) if device_data is not None else 5
        self.proximity_counter = 0

    def sensors_reading(self):
        print('timer {0}'.format(self.timer))
        while True:
            timestamp = time() * 1000
            readings = self.__read_sensors()
            self.database_manager.save_readings(timestamp, readings)

    def set_timer(self, device_json_data):
        seconds = self.__translate_json_time(device_json_data['timeValue'], device_json_data['timeUnit'])
        self.timer = seconds

    def __read_sensors(self):
        readings = {}

        for sensor_type in self.sensors:
            read_method = self.sensors[sensor_type]['read_method']
            sensor = self.sensors[sensor_type]['object']

            reading = read_method(sensor)
            readings[sensor_type] = reading

        print(readings)
        return readings

    def __translate_json_time(self, value, unit):
        units = [('SECONDS', 1), ('MINUTES', 60), ('HOURS', 60 * 60), ('DAYS', 24 * 60 * 60)]

        for possible_unit in units:
            if possible_unit[0] == unit:
                return possible_unit[1] * value

        return 1
    
    def __set_proximity_sensor(self):
        return machine.Pin(2, machine.Pin.IN)

    def __read_proximity(self, sensor):
        initial_time = time()

        while True:
            if time() - initial_time >= self.timer:
                #print(self.proximity_counter)
                return self.proximity_counter
            
            if self.__new_day():
                old_proximity_counter = self.proximity_counter
                self.proximity_counter = 0

                return old_proximity_counter

            reading = sensor.value()
            self.proximity_counter += 1 if reading == 0 else 0
            sleep(0.05)
    
    def __new_day(self):
        local_time = localtime()
        return local_time[3] == 0 and local_time[4] < 1 and local_time[5] < 3
    
    def __set_internal_sound_sensor(self):
        return machine.ADC(26)

    def __read_internal_sound(self, sensor):
        return sensor.read_u16()
    
    def __set_external_sound_sensor(self):
        return machine.ADC(27)
    
    def __read_external_sound(self, sensor):
        return sensor.read_u16()

    # def __read_bem680(self):
    #     sensor = self.__set_bme680()

    #     if sensor.get_sensor_data():
    #         output = '{0:.2f} C,{1:.2f} hPa,{2:.3f} %RH'.format(
    #             sensor.data.temperature,
    #             sensor.data.pressure,
    #             sensor.data.humidity)
    #         print(output)

    # def __set_bme680():
    #     try:
    #         sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
    #     except (RuntimeError, IOError):
    #         sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        
    #     sensor.set_humidity_oversample(bme680.OS_2X)
    #     sensor.set_pressure_oversample(bme680.OS_4X)
    #     sensor.set_temperature_oversample(bme680.OS_8X)
    #     sensor.set_filter(bme680.FILTER_SIZE_3)

    #     return sensor
    
