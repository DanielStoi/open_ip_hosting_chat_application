#!/bin/python
import signal
import os
import sys
import socket
import select
import hashlib


daemon_quit = False


#Do not modify or remove this handler
def quit_gracefully(signum, frame):
    global daemon_quit
    daemon_quit = True

def hash_alg(text):
    return str(int(hashlib.md5(text.encode('utf-8')).hexdigest(), 16))





    




def process_text(text):
    lines = text.split('\n')
    ans = list()
    for i in lines:
        if len(i)>2:
            ans.append(i.split())
    #print("processed text is",ans)
    return ans


class App():
    def __init__(self):
        self.messages = {None : list()} #socket->messagelist
        self.accounts = {} #username->socket
        self.channels = {} #channelname->usernames
        self.user_db = list()


    def process_cmd(self,connection, cmd):
        messages = self.messages
        print("attempting to process:\n",cmd)
        ## PROCESSING INPUT ##
        
        if cmd[0] == "LOGIN":
            if len(cmd)==3:
                if self.login(connection,cmd[1],cmd[2]):
                    messages[connection].append("RESULT LOGIN 1\n")
                    return
            messages[connection].append("RESULT LOGIN 0\n")

        elif cmd[0] == "REGISTER":
            #print("entering register")
            if len(cmd)>=3:
                #print("register format was valid")
                if self.register(cmd[1],cmd[2]):
                    messages[connection].append("RESULT REGISTER 1\n")
                    return
            messages[connection].append("RESULT REGISTER 0\n")
        
        elif cmd[0] == "JOIN":
            if len(cmd)>1: 
                if self.join_channel(connection,cmd[1]):
                    messages[connection].append("RESULT JOIN %s 1\n" % cmd[1])
                else:
                    messages[connection].append("RESULT JOIN %s 0\n" % cmd[1])

        elif cmd[0] == "CREATE":
            if len(cmd)>1:
                new_channel_name = cmd[1]
                if self.create_channel(new_channel_name):
                    messages[connection].append("RESULT CREATE %s 1\n" % cmd[1])
                    return
                messages[connection].append("RESULT CREATE %s 0\n" % cmd[1])
                
        elif cmd[0] == "CHANNELS":
            channel_names = list(self.channels.keys())
            channel_names.sort()
            messages[connection].append("RESULT CHANNELS "+", ".join(channel_names)+"\n")
        
        
        elif cmd[0] == "SAY":
            #say shouldn't have result return
            if len(cmd)>=3:
                message = " ".join(cmd[2:])
                if (self.write_to_channel(cmd[1],connection,message)):
                    return
            messages[connection].append("INVALID MESSAGE\n")
                

        else:
            self.messages[connection].append("INVALID COMMAND\n")

    def find_user_from_socket(self, s):
        for username in self.accounts:
            if self.accounts[username]==s:
                return username
        return None
    
    def add_user(self,s):
        if not s in self.messages:
            self.messages[s] = list()

    def delete_user(self,s):
        if s in self.messages: self.messages.pop(s)
        if s in self.accounts: self.accounts.pop(s)
        for channel in self.channels:
            if s in channel: channel.remove(s)
        name = self.find_user_from_socket(s)
        if name != None:
            self.accounts[name]= None
        


    def login(self,connection, username,password):
        #print(self.user_db)
        if username in self.accounts and self.accounts[username] != None:
            return False
        

        for user in self.user_db:
            if user[0] == username:
                if hash_alg(password) == user[1]:
                    self.accounts[username]=connection
                    return True
        return False


    def register(self,username,password):
        #print(self.user_db)
        for user in self.user_db:
            if user[0] == username:
                return False
        password = hash_alg(password)
        self.user_db.append((username, password))
        return True

    def join_channel(self,connection,channelname):
        if not channelname in self.channels:
            return False
        username = self.find_user_from_socket(connection)
        if not username:
            return False
        if username in self.channels[channelname]:
            return False
        self.channels[channelname].append(username)
        return True




    def create_channel(self,channelname):
        if channelname in self.channels:
            return False
        self.channels[channelname] = list()
        return True


    def write_to_channel(self, channelname,connection,message):
        username = self.find_user_from_socket(connection)
        if not username:
            return False

        message = "RECV "+username+" "+channelname+" "+message+"\n"
        if not channelname in self.channels:
            return False
        if not username in self.channels[channelname]:
            return False

        for user in self.channels[channelname]:
            if user in self.accounts and self.accounts[user]:
                self.messages[self.accounts[user]].append(message)
        return True






def run(ip='localhost',port=6025):
    #Do not modify or remove this function call
    signal.signal(signal.SIGINT, quit_gracefully)
    print("\n\n###\nTHIS IS THE SERVER APPLICATION FOR THE CHAT APP\n###")
    ##################################################
    #SETUP
    ##################################################


    print("attempted startup")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server_address = ('localhost', port)
    server.bind(server_address)
    
    server.listen(5)
    inputs = [server]
    outputs = list()
    print("\nRUNNING")
    app = App()

    
    ##################################################
    #MAIN LOOP
    ##################################################
    while not daemon_quit:
        read_ready, write_ready, exceptions = select.select(inputs, outputs, inputs,0.01)

        for s in read_ready:
            # accept connection if server is read-ready
            if s is server:
                connection, client_address = s.accept()
                connection.setblocking(False)
                print ("server received connection: socket " + str(client_address))
                inputs.append(connection)
                outputs.append(connection)
                app.add_user(connection)
            # receive message if a connection is read-ready
            else:
                #print("attempting to receive message;")
                message = False
                try:
                    message = s.recv(1024)
                    if message:
                        
                        message = message.decode("utf-8") 
                        print("message is", message)
                        for cmd in process_text(message):
                            app.process_cmd(s,cmd)
                except:
                    s.close()
                    inputs.remove(s)
                    outputs.remove(s)
        
        for s in write_ready:
            try:
                if s in app.messages and app.messages[s]:
                    message = app.messages[s].pop(0)
                    s.send(message.encode())
            except:
                pass 
        
    server.close()
                    
                

            
            
    


if __name__ == '__main__':
    ip = 'localhost'
    port = 6025
    if len(sys.argv)<2:
        print("ip and port not specified, will attempt to run on localhost, port 6025")
    else:
        if len(sys.argv<3):
            port = int(sys.argv)
            print("ip not specified, will assume that it runs on localhost")
        else:

            port = int(sys.argv[2])
            ip = sys.argv[1]
    run(ip,port)

