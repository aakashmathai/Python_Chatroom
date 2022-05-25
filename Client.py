import socket, threading


class Client:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.username = ""
        self.flag = True
        self.receive_thread = None
        self.write_thread = None

    def receive(self):
        while self.flag:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message.startswith("/username="):
                    self.username = message.split("=")[1].split(" ")[0].strip(" ")
                    print("Your user name is " + str(self.username) + "\n")
                elif message.endswith("/QUIT"):
                    self.client.close()
                    self.flag = False
                    print("DISCONNECTED!!")
                    break
                else:
                    print(message)
            except:
                print("An error occured!")
                self.client.close()
                self.flag = False
                break

    def write(self):
        while self.flag:  # message layout
            try:
                message = '{}: {}'.format(self.username, input(''))
                self.client.send(message.encode('ascii'))
            except:
                break

    def process(self):
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()
        self.write_thread = threading.Thread(target=self.write)
        self.write_thread.start()


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 7976
    obj = Client(host, port)
    obj.process()
