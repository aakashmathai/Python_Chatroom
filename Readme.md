# What

Client server program written using socket programming in python. This program allows to create a chatroom server using
the [Server.py](Server.py) file. Once the server starts listening, multiple clients can join the chatroom using
[Client.py](Client.py) file.

## Server.py

The host IP address and port number were passed as parameters to the Server python class. The library functions from the
package socket were used to start a server, and the given host and port were bound to the server.

The server class includes functions for the broadcast command, help command, users command, dm command, and quit
command, as well as other supporting functions.

When the server is ready, it begins to accept connections. When a client asks the server for a connection, the request
is accepted and the client is added to a list of clients. A username is generated and sent to the connected client. In
addition, a message is broadcast to all existing connected clients informing them of the newly joined client.

When a client connects to the server, a thread is launched that will continue to listen to the client indefinitely. When
a client message is received, the command portion is extracted and the appropriate action is taken. Following certain
data manipulations, the actions are function calls.

When a client disconnects from the server, the socket connection is closed and the thread execution for that client is
automatically completed.

## Client.py

A Python class called Client is defined. It also receives the IP address and port number of the host as parameters. When
a class object is created with an IP address and port number, it connects to an already running server.

When you run the client program, two threads are started: one for sending messages and one for receiving messages from
the server. The client anticipates receiving an initial message from the server, which will be used to extract the
username.

The client program is constantly seeking user input. When a user types in a command, it is sent to the server. The
server responds to client requests and sends responses or new messages.

## Commands

| Command      | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| /help        | Print out all supported commands                                |
| /users       | print list of all connected users                               |
| /dm          | send direct message to a user. Syntax = /dm username "message"  |
| /bc          | broadcast a message. Syntax = /bc "message"                     |
| /quit        | disconnect from server                                          |