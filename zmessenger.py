import socket
import json

def send_messages(ip, port, messages):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))

            s.sendall(messages[0].encode('utf-8'))
            print(f"Message 1 sent: {messages[0]}")

            # # Receive data from the server (optional)
            # data = s.recv(1024)
            # print(f"Received from server: {data.decode('utf-8')}")

            # Send the second message
            # s.sendall(messages[1].encode('utf-8'))
            # print(f"Message 2 sent: {messages[1]}")

            # Receive data from the server (optional)
            data = s.recv(2048)
            print(f"Received from server: {data.decode('utf-8')}")

    except Exception as e:
        print(f"Error: {e}")

a = {
    "id": "salve o corinthians",
    "location": {
        "longitude": -59.3453,
        "latitude": -77.82653
    },
    "name": "Unicamp",
    "frequencyOfSavingData": {
        "timeUnit": "SECONDS",
        "timeValue": 1
    }
}
message2 = json.dumps(a)
message1 = 'GET /device HTTP/1.1\r\nuser-agent: Dart/3.1 (dart:io)\r\ncontent-type: application/json; charset=UTF-8\r\naccept-encoding: gzip\r\nhost: 10.0.0.103\r\n\r\n'
send_messages('10.0.0.103',80,[message1, message2])