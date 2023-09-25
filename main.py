import machine
import ssd1306
import utime
from do_connect import *
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
import re
# Definindo o tempo de debouncing em milissegundos
DEBOUNCE_MS = 200

# Configurando o pino do sensor de proximidade como entrada
proximity_sensor = machine.Pin(2, machine.Pin.IN)

# Definindo as cores do LED RGB
red = machine.Pin(6, machine.Pin.OUT)
green = machine.Pin(7, machine.Pin.OUT)
blue = machine.Pin(5, machine.Pin.OUT)

# Inicializando o display OLED
i2c = machine.I2C(1, scl=machine.Pin(19), sda=machine.Pin(18))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# Configurando os botões A e B como entrada com pull-up interno
button_a = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
button_b = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)

# Desligando todas as cores do LED
red.value(0)
green.value(0)
blue.value(0)

# Inicialmente, definir LED para azul
blue.value(1)

# Inicializando a contagem de objetos detectados
object_count = 0

# Variável para armazenar o estado anterior do sensor
previous_state = 0

# Modo de decremento, inicialmente desativado
decrement = False

# Temporizador para o botão B
last_b_press = utime.ticks_ms() - DEBOUNCE_MS

def text_center(message, line):
    message_width = len(message) * 8  # O display tem uma largura de 8 pixels por caractere
    x_position = max((display.width - message_width) // 2, 0)
    display.text(message, x_position, line * 10)

def display_count():
    display.fill(0)
    display.text('Objetos Detec:', 0, 0)
    text_center(str(object_count), 1)
    display.text('A:reset B:invert', 0, 25)
    display.show()
    
def try_connect_to_Wifi(ssid, password):
    blue.value(0)
    display.fill(0)
    display.text('Wifi', 0, 0)
    try:
        ip = do_connect(ssid, password)
        display.text(f'Connected to {ip}', 0, 15)
        green.value(1)
    except:
        display.text('error', 0, 0)
        red.value(1)
    display.show()

def get_Wifi_information_from_bluetooth(received_string):
    # Remova o "b'" no início e o "'" no final
    received_string = received_string[2:-1]

    # Divida a string usando "|" como delimitador para obter partes
    parts = received_string.split('|')

    # Crie um dicionário para armazenar os valores
    values = {}

    # Divida cada parte usando ":" como delimitador e armazene os valores no dicionário
    for part in parts:
        key, value = part.split(':')
        values[key] = value

    # Recupere os valores de ssid e password do dicionário
    ssid = values.get('ssid')
    password = values.get('password')
    return ssid, password
    
# Create a Bluetooth Low Energy (BLE) object
ble = bluetooth.BLE()

# Create an instance of the BLESimplePeripheral class with the BLE object
sp = BLESimplePeripheral(ble)

# Define a callback function to handle received data
def on_rx(data):
    print("Data received: ", data)  # Print the received data
    received_string = data.decode('utf-8')
    print("received_string")
    if received_string == "toggle": 
        blue.value(0)
        green.value(1)
        
    #regex_pattern = r'^ssid:[\w]+|password:[\w]+$'
    #match = re.match(regex_pattern, received_string)
    #if(match):
     #   print("information matched!")
      #  ssid, password = get_Wifi_information_from_bluetooth(received_string);
       # try_connect_to_Wifi(ssid, password)
print("start bluetooth")
# Start an infinite loop
while True:
    if sp.is_connected():  # Check if a BLE connection is established
        sp.on_write(on_rx)  # Set the callback function for data reception

    

while False:
    # Se o sensor de proximidade detectar um objeto próximo,
    # mude a cor do LED para vermelho e altera a contagem
    if proximity_sensor.value() and not previous_state:
        red.value(1)
        blue.value(0)
        if decrement:
            object_count -= 1
        else:
            object_count += 1
        previous_state = 1

        # Mostrar a contagem de objetos detectados
        display_count()

    elif not proximity_sensor.value():
        blue.value(1)
        red.value(0)
        previous_state = 0

    # Se o botão A for pressionado, zere a contagem
    if not button_a.value():
        object_count = 0
        display_count()
        
    # Se o botão B for pressionado, alternar o modo de decremento
    if not button_b.value() and utime.ticks_diff(utime.ticks_ms(), last_b_press) > DEBOUNCE_MS:
        decrement = not decrement
        last_b_press = utime.ticks_ms()




