import signal
import os
import socket
import select

#note: currently alot of placeholder functions
#this section will be done after the main application is complete


class ClientConnection():
    def __init__(self):
        self.messages = list()
        self.out_queue = list()
        self.changed = False

    def connect(self,host,port):
        try:
            port = int(port)
            return True
        except:
            return False

        this.host = host
        this.port = port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ret = s.connect_ex((host,port))
        if ret!=0:
            print("failed to connect")
            return False

        s.setblocking(False)
        self.inputs = [s]
        self.outputs = [s]
        self.s = s
        return True

    def update(self):
        return True
        read_ready, write_ready, exceptions = select.select(inputs, outputs, inputs,0.01)

        for s in read_ready:
            # accept connection if server is read-ready
            if s is self.s:
                connection, client_address = s.accept()
                connection.setblocking(False)
                print ("server received connection: socket " + str(client_address))
                self.inputs.append(connection)
                self.outputs.append(connection)
            # receive message if a connection is read-ready
            else:
                #print("attempting to receive message;")
                message = s.recv(1024)
                
                if message:
                    message = message.decode("utf-8") 
                    self.messages.append(message)
                else:
                    s.close()
                    self.inputs.remove(s)
                    self.outputs.remove(s)
        
        for s in write_ready:
            if self.messages:
                message = self.out_queue.pop(0)
                s.send(message.encode())

    def write(self,message):
        self.out_queue.append(message)
    
    def get_messages(self):
        self.messages.append("RECV joe test this is a pratice message")
        ans = self.messages
        self.messages = list()
        return ans

    def has_changed(self):
        if self.changed:
            self.changed = False
            return True
        return False

    def login(self,usrname,password):
        self.out_queue.append("LOGIN "+str(usrname)+" "+str(password))
        
        #TEMP
        self.messages.append("RESULT LOGIN 1")
        self.changed = True
        
    def logout(self):
        self.out_queue.append("LOGOUT")


        #TEMP
        self.messages.append("RESULT LOGOUT 1")
        self.changed = True
        
        

        
        
    
