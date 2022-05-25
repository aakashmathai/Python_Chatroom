import socket, threading
import time


class Server:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.usernames = []
        self.count = 0
        print("Server started on host {} and port {}".format(host,port))

    def client_lookup(self, name):
        index = self.usernames.index(name)
        client = self.clients[index]
        return client

    def broadcast_command(self, message, sender):  # broadcast function declaration
        for client in self.clients:
            if client != sender:
                client.send(message)

    def help_command(self, sender):
        available_commands = '''
        /help - print this message
        /users - print list of all connected users
        /dm - send direct message to a user. Syntax = /dm username "message"
        /bc - broadcast a message. Syntax = /bc "message"
        /quit - disconnect from server
        '''
        sender.send(available_commands.encode('ascii'))

    def users_command(self, sender):
        sender.send(str(self.usernames).encode('ascii'))

    def dm_command(self, target, message):
        target.send(message)

    def quit_command(self, sender):
        sender.send("You will be disconnected from the server".encode('ascii'))
        sender.send("/QUIT".encode('ascii'))
        index = self.clients.index(sender)
        self.clients.remove(sender)
        user = self.usernames[index]
        self.usernames.remove(user)
        sender.close()
        self.broadcast_command('{} left!'.format(user).encode('ascii'), None)
        print('{} left!'.format(user))

    def process(self, message, sender):
        username = str(message.decode('ascii')).split(':')[0].strip(" ")
        command = str(message.decode('ascii')).split(':')[1].strip(" ").split(" ")[0].strip(" ")
        if command == "/help":
            self.help_command(sender)
        elif command == "/users":
            self.users_command(sender)
        elif command == "/dm":
            target = str(message.decode('ascii')).split(':')[1].strip(" ").split(" ")[1].strip(" ")
            if target in self.usernames:
                target_socket = self.client_lookup(target)
                dm_message = (username + " <dm> : " + str(message.decode('ascii')).split(':')[1].strip(" ").lstrip(
                    "/dm").strip(" ").lstrip(target).lstrip(" ")).encode('ascii')
                self.dm_command(target_socket, dm_message)
            else:
                err_msg = target + " is not connected"
                self.dm_command(sender, err_msg.encode('ascii'))
        elif command == "/bc":
            bc_msg = str(message.decode('ascii')).split(':')[1].strip(" ").lstrip('/bc')
            self.broadcast_command((username + " <bc> : " + bc_msg).encode('ascii'), self.client_lookup(username))
        elif command == "/quit":
            self.quit_command(sender)
        else:
            sender.send("INVALID COMMAND".encode('ascii'))

    def handle(self, client):
        while True:
            try:  # recieving valid messages from client
                message = client.recv(1024)
                self.process(message, client)
            except:  # removing clients
                if client in self.clients:
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
                    user = self.usernames[index]
                    self.broadcast_command('{} got disconnected!'.format(user).encode('ascii'), None)
                    print('{} got disconnected from server!'.format(user))
                    self.usernames.remove(user)
                break

    def incoming(self):  # accepting multiple clients
        while True:
            client, address = self.server.accept()
            print("Connected with {}  ".format(str(address)))
            self.count = self.count + 1
            username = "user" + str(self.count)
            client.send(('/username=' + username).encode('ascii'))
            self.usernames.append(username)
            self.clients.append(client)
            print("Username {} joined".format(username))
            self.broadcast_command("{} joined!   ".format(username).encode('ascii'), client)
            time.sleep(1)
            client.send('   Connected to server!'.encode('ascii'))
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()


if __name__ == '__main__':
    host = '127.0.0.1'  # LocalHost
    port = 7976

    obj = Server(host, port)
    obj.incoming()
