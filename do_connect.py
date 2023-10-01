import network
import time
import socket
def do_connect_to_wifi(ssid, psk):
    print('try connect to wifi')
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, psk)

    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    
    print('Connection Success!')
    ip = wlan.ifconfig()[0]
    return ip

def open_socket(ip):
    print('Opening socket')
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection
