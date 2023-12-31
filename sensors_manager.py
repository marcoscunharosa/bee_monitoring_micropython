import machine
from time import sleep, localtime, time
import ujson
from lib.bme680 import BME680_I2C
class SensorsManager:
    def __init__(self, database_manager, device_data=None) -> None:
        bme680_internal, bme680_external = self.__try_to_set_bme680()
        self.sensors = {
            'proximity': {'object': self.__set_proximity_sensor(), 'read_method': self.__read_proximity},
            'internal_sound': {'object': self.__set_internal_sound_sensor(), 'read_method': self.__read_internal_sound},
            'external_sound': {'object': self.__set_external_sound_sensor(), 'read_method': self.__read_external_sound},
            'internal_temperature': {'object': bme680_internal, 'read_method': self.__read_temperature},
            'internal_pressure': {'object': bme680_internal, 'read_method': self.__read_pressure},
            'internal_humidity': {'object': bme680_internal, 'read_method': self.__read_humidity},
            'internal_gas': {'object': bme680_internal, 'read_method': self.__read_gas},
            'external_temperature': {'object': bme680_external, 'read_method': self.__read_temperature},
            'external_pressure': {'object': bme680_external, 'read_method': self.__read_pressure},
            'external_humidity': {'object': bme680_external, 'read_method': self.__read_humidity},
            'external_gas': {'object': bme680_external, 'read_method': self.__read_gas}
        }

        self.database_manager = database_manager
        if device_data is not None:
            self.set_timer(device_data['frequencyOfSavingData'])
        else:
            self.timer = 60
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

    def __read_temperature(self, bme):
        if bme is None:
            return None
        else:
            return bme.temperature
    
    def __read_humidity(self, bme):
        if bme is None:
            return None
        else:
            return bme.humidity

    def __read_pressure(self, bme):
        if bme is None:
            return None
        else:
            return bme.pressure
    
    def __read_gas(self, bme):
        if bme is None:
            return None
        else:
            return bme.gas

    def __set_bme680_internal(self):
        i2c = machine.I2C(0, scl=machine.Pin(21), sda=machine.Pin(20))
        bme = BME680_I2C(i2c=i2c)
        return bme
    def __set_bme680_external(self):
        i2c = machine.I2C(0, scl=machine.Pin(25), sda=machine.Pin(24))
        bme = BME680_I2C(i2c=i2c)
        return bme
    
    def __try_to_set_bme680(self):
        bme680_internal = None
        bme680_external = None
        try:
            bme680_internal = self.__set_bme680_internal()
            bme680_external = self.__set_bme680_external()
        except Exception as e:
            print('bme bad functioning')
        return bme680_internal, bme680_external
    

