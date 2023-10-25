import machine
from time import sleep

class SensorsManager:
    def __init__(self, database_manager) -> None:
        self.sensor_reading_methods = [
            self.__read_proximity_sensor,
            self.__read_internal_sound_sensor,
            self.__read_external_sound_sensor,
            # self.__read_bem680
        ]
        self.database_manager = database_manager
        self.proximity_sensor_is_detecting = False

    def sensors_reading(self):
        #teste
        for i in range(14):
            readings = self.__read_sensors()
            self.database_manager.save(i, readings)
            print(readings)
            sleep(1)

        #real
        # while True:
        #     timestamp = 1
        #     readings = self.__read_sensors()
        #     self.database_manager.save(timestamp, readings)

    def __read_sensors(self):
        readings = []
        for sensor_reading_method in self.sensor_reading_methods:
            reading = sensor_reading_method()
            readings.append(reading)
        
        return readings

    def __read_proximity_sensor(self):
        sensor = machine.Pin(2, machine.Pin.IN)
        value = sensor.value()

        return self.__new_proximity_detection(value)
    
    def __new_proximity_detection(self, sensor_value):
        if sensor_value == 0 and not self.proximity_sensor_is_detecting:
            self.proximity_sensor_is_detecting = True
            return 1
        elif sensor_value == 1:
            self.proximity_sensor_is_detecting = False
        
        return 0
    
    def __read_internal_sound_sensor(self):
        adc = machine.ADC(26)
        return adc.read_u16()
    
    def __read_external_sound_sensor(self):
        adc = machine.ADC(27)
        return adc.read_u16()

    def __read_bem680(self):
        pass