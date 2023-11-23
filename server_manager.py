import ujson

class ServerManager:
    def __init__(self, connection, database, sensors_manager):
        self.connection = connection
        self.database = database
        self.sensors_manager = sensors_manager

    def listen_to_connections(self):
        print("Listening to connections...")
        while True:
            client, addr = self.connection.accept()
            print('Got a connection from %s' % str(addr))
            try:
                header_request = client.recv(1024)
                instruction, timestamp_start_filter, timestamp_end_filter = self.__decode_instruction(header_request.decode('utf-8'))
                self.__do_instruction(client, instruction, timestamp_start_filter, timestamp_end_filter)
            except Exception as e:
                print("Server manager error: ", e)
                client.close()
                continue

    def __decode_instruction(self, header):
        command =  header.split(' ')[1][1:]
        aux = command.split('?')

        if len(aux) == 1:
            return command, None, None

        instruction = aux[0]
        start_filter = int(aux[1].split('{')[1][:-1])

        if len(aux) == 2:
            return instruction, start_filter, None
        
        end_filter = int(aux[2].split('{')[1][:-1])
        return instruction, start_filter, end_filter
    

    def __do_instruction(self, client, instruction, timestamp_start_filter, timestamp_end_filter):
        if instruction == "register":
            data = client.recv(1024).decode('utf-8')
            self.database.save_device(data)

            json_data = ujson.loads(data)
            self.sensors_manager.set_timer(json_data["frequencyOfSavingData"])

            self.__send_response(client, 200, "OK")
        elif instruction == "device":
            self.__send_response(client, 200, "OK", "application/json", self.database.get_device_data())
        elif instruction == "data":
            self.__send_response(client, 200, "OK", "application/json", self.database.get_readings(timestamp_start_filter, timestamp_end_filter))
        elif instruction == "clear":
            self.database.clear()
            self.__send_response(client, 200, "OK")
        else:
            self.__send_response(client, 404, "Not Found")

    def __send_response(self, client, status_code, status_message, content_type = None, content = None):
        response = "HTTP/1.1 {0} {1}\r\n".format(status_code, status_message)

        if content_type is not None:
            response += "Content-Type: {0}\r\n".format(content_type)
        if content is not None:
            response += "Content-Length: {0}\r\n".format(len(content))
        response += "\r\n"
        if content is not None:
            response += content

        client.send(response)
        client.close()

