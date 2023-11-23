import socket
import json

def send_messages(ip, port, messages):
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to the server (IP address and port)
            s.connect((ip, port))

            # Send the first message
            s.sendall(messages[0].encode('utf-8'))
            print(f"Message 1 sent: {messages[0]}")

            # # Receive data from the server (optional)
            # data = s.recv(1024)
            # print(f"Received from server: {data.decode('utf-8')}")

            # Send the second message
            # s.sendall(messages[1].encode('utf-8'))
            # print(f"Message 2 sent: {messages[1]}")

            # Receive data from the server (optional)
            data = s.recv(1024)
            print(f"Received from server: {data.decode('utf-8')}")

    except Exception as e:
        print(f"Error: {e}")

a = {
    "id": "5d0cdb5d-fc1e-48ff-a69b-88aaa44e1er5",
    "location": {
        "longitude": -47.07645,
        "latitude": -22.82653
    },
    "name": "New Device 2",
    "frequencyOfSavingData": {
        "timeUnit": "MINUTES",
        "timeValue": 15
    }
}
message2 = json.dumps(a)
send_messages('10.0.0.103',80,['GET /device HTTP/1.1', message2])
# ?until={5}