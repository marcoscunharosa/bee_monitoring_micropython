import ujson
class BeeServer:

    def __init__(self, connection, database):
        self.connection = connection
        self.database = database

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
        return header.split(' ')[1][1:]

    
    def __do_instruction(self, client, instruction):
        if instruction == "register":
            data = client.recv(1024).decode('utf-8')
            json_data = ujson.loads(data)
            print(json_data)
            self.__send_response(client, 200, "OK")
        elif instruction == "data":
            self.__send_response(client, 200, "OK", "application/json", self.database.get_data)
        else:
            self.__send_response(client, 404, "Not Found")
    
    def listen_to_connections(self):
        print("Listening to connections...")
        while True:
            client, addr = self.connection.accept()
            print('Got a connection from %s' % str(addr))
            try:
                header_request = client.recv(1024)
                instruction = self.__decode_instruction(header_request.decode('utf-8'))
                print(instruction)
                self.__do_instruction(client, instruction)
            except:
                print("Error")
                client.close()
                continue
