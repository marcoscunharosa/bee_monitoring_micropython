import ujson
class BeeServer:

    def __init__(self, connection, database, sensors_manager):
        self.connection = connection
        self.database = database
        self.sensors_manager = sensors_manager

    def __send_response(self, client, status_code, status_message, content_type = None, content = None):
        response = "HTTP/1.1 {0} {1}\r\n".format(status_code, status_message)
        if content_type is not None:
            response += "Content-Type: {0}\r\n".format(content_type)
        if content is not None:
            response += "Content-Length: {0}\r\n".format(len(content))
        response += "\r\n"
        if content is not None:
            response += content

        print('response: ', response)
        client.send(response)
        client.close()

    def __decode_instruction(self, header):
        print('header: ', header)
        instuction =  header.split(' ')[1][1:]
        if 'until' in instuction:
            timestamp_lower_bound = int(instuction.split('{')[1][:-1])
            return 'data', timestamp_lower_bound

        return instuction, 0

    def __do_instruction(self, client, instruction, timestamp_lower_bound):
        if instruction == "register":
            data = client.recv(1024).decode('utf-8')
            self.database.save_device(data)

            json_data = ujson.loads(data)
            self.sensors_manager.set_timer(json_data["frequencyOfSavingData"])

            self.__send_response(client, 200, "OK")
        elif instruction == "device":
            self.__send_response(client, 200, "OK", "application/json", self.database.get_device_data())
        elif instruction == "data":
            self.__send_response(client, 200, "OK", "application/json", self.database.get_data(timestamp_lower_bound))
        elif instruction == "clear":
            self.database.clear()
            self.__send_response(client, 200, "OK")
        else:
            self.__send_response(client, 404, "Not Found")
    
    def listen_to_connections(self):
        print("Listening to connections...")
        while True:
            client, addr = self.connection.accept()
            print('Got a connection from %s' % str(addr))
            try:
                header_request = client.recv(1024)
                instruction, timestamp_filter = self.__decode_instruction(header_request.decode('utf-8'))
                self.__do_instruction(client, instruction, timestamp_filter)
            except Exception as e:
                print("bee_server errror = ", e)
                client.close()
                continue
