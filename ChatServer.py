import socket
import select
import sys
from thread import *
import re
 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 
IP = "127.0.0.1"
Port = 7000
server.bind((IP, Port))
server.listen(100)
 
#list_of_clients = []
list_of_groups = []
 
def clientthread(conn, addr):
 
    conn.send("Welcome to this chatroom!\n")
    conn.send("To create a new group type 'n' before the name of the group.\n")
    conn.send("To join a group type 'j' before the name of the group.\n")
    filename = None
    while True:
            try:
                message = conn.recv(2048)
                shouldbreak = False
                #If the incoming message starts with an 'n' the if statement will run
                if message.split()[0] == "n":
                    #Splits the message and stores everything besides 'n' into nameoffile
                    nameoffile = message.split(' ', 1)[1]
                    #Will run the code only if there is one word in nameoffile, else it will tell the user only to input one word after 'n'
                    if len(nameoffile.split()) == 1:
                        #strips '\n'
                        newfilename = re.sub('\W+','', nameoffile )
                        #Runs through list_of_groups to see in a user is already apart 
                        for gr in list_of_groups:
                            if gr.groupname == newfilename:
                                conn.send("Group already exists!")
                                shouldbreak = True
                                break
                        if shouldbreak == True:
                            continue
                        if filename is not None:
                            removefromgroup(conn, filename)
                        filename = newfilename
                        newg = Group(filename)
                        newg.joingroup(conn)
                        list_of_groups.append(newg)
                    else:
                        connection.sendall("Only one word can be specified after 'n' for the name of the group!")
                elif message.split()[0] == "j":
                    nameoffile = message.split(' ', 1)[1]
                    if len(nameoffile.split()) == 1:
                        newfilename = re.sub('\W+','', nameoffile )
                        numberofgroups = len(list_of_groups)
                        groupcount = 0
                        for gr in list_of_groups:
                            if gr.groupname != newfilename:
                                groupcount += 1
                        if numberofgroups == groupcount:
                            conn.send("You must create a new group before you join one.")
                            continue
                        for gr in list_of_groups:
                            if gr.groupname == newfilename:
                                if conn in gr.conn:
                                    conn.send("You are already in this group!")
                                    shouldbreak = True
                                    break
                        if shouldbreak == True:
                            continue
                        if filename is not None:
                            removefromgroup(conn, filename)
                        filename = newfilename
                        for gr in list_of_groups:
                            if gr.groupname == filename:
                                gr.joingroup(conn)
                elif filename == None:
                    conn.send("You must create a new group with 'n' or join a group with 'j' | Type 'n' or 'j' and then one word for the name of the group!")
                elif message:
                    print addr[0] + " | " + message
                    sendmessage = addr[0] + " | " + message
                    broadcast(sendmessage, conn, filename)
                else:
                    #remove(conn)
                    try:
                        removefromgroup(conn, filename)
                    except:
                        continue          
            except:
                continue
 
# def remove(connection):
#     if connection in list_of_clients:
#         list_of_clients.remove(connection)

def removefromgroup(conn, filename):
    for gr in list_of_groups:
        if gr.groupname == filename:
            gr.conn.remove(conn)
        
def broadcast(message, connection, filename):
    for gr in list_of_groups:
        if gr.groupname == filename:
            for client in gr.conn:
                if client!=connection:
                    try:
                        client.send(message)
                    except:
                        client.close()
                        #remove(client)

class Group(object):
    def __init__(self, groupname):
        self.groupname = groupname
        self.conn = []

    def joingroup(self, connec):
        self.connec = connec
        self.conn.append(self.connec)
        #print self.connec, "hi"
 
while True:
    conn, addr = server.accept()
    #list_of_clients.append(conn)
    print addr[0] + " connected"
    start_new_thread(clientthread,(conn,addr))    
 
conn.close()
server.close()