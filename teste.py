from lib.bme680 import *
from machine import I2C, Pin
import time

i2c = I2C(0, scl=Pin(21), sda=Pin(20))
i2c_ext = I2C(0, scl=Pin(25), sda=Pin(24))
print('iniciating bme')
bme = BME680_I2C(i2c=i2c)
for _ in range(3):
    print(bme.temperature, bme.humidity, bme.pressure, bme.gas)
    time.sleep(1)
