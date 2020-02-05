import socket
import select
import sys
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HostIP = "127.0.0.1"
Port = 7000
server.connect((HostIP, Port))
 
while True:
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            if message == "":
                exit()
            print message
        else:
            message = sys.stdin.readline()
            if message == "exit\n":
                server.close()
                exit()
            server.send(message)
            # sys.stdout.write("You | ")
            # sys.stdout.write(message)
            # sys.stdout.flush()

server.close()