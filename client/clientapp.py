from tkinter import *
import clientnet
win = Tk()
acc = None #account if logged in
conn = None #network connection to server
messages = list()
MAX_MESSAGES = 20
groot = None

notification = " "
########
#Helper
########

def interpret_input(s):
    if "RESULT LOGIN" == s[:12]:
        if "1" in s:
            global acc
            acc = True
    elif "RECV" == s[:4]:
        
        message = s[5:]
        message = message.split()

        
        if len(message)>=3:
            message = "USER: "+message[0]+" CHANNEL:"+ message[1]+"\tSAID: " +" ".join(message[2:])
            messages.append(message)
        else:
            messages.append(" ".join(message))

        if len(messages)>MAX_MESSAGES:
            messages.pop(0)
    else:
        global notification
        notification = s



        

def wipe_frame(frame):
    for item in frame.winfo_children():
      item.destroy()
########
#ROUTES
########




########
#Connection screen
########



            
def join_create_channel():
    wipe_frame(groot)
    root = groot

    instr = Label(root, text="create/join channel")
    instr.grid(row=0,column=0)
    usr = Entry(root)
    
    usr.grid(row=1,column=0)
    usr.insert(0,"Channel Name")


    def send_join_signal():
        channel_name = usr.get()
        conn.write("JOIN "+channel_name)
        go_to_home()
    
    def send_create_signal():
        channel_name = usr.get()
        conn.write("CREATE "+channel_name)
        conn.write("JOIN "+channel_name)
        go_to_home()

    jB = Button(root,text="Join",command=send_join_signal)
    jB.grid(row=2,column=0)

    cB = Button(root,text="Create",command=send_create_signal)
    cB.grid(row=2,column=1)

    cancelB = Button(root,text="Cancel",command=go_to_home)
    cancelB.grid(row=3,column=0)

    win.title("chatApp -create/join channel")

    



def logout():
    
    global acc
    acc = None
    conn.logout()
    home(groot)

def login(root):
    instr = Label(root, text="login to account")
    instr.grid(row=0,column=0)
    usr = Entry(root)
    usr.grid(row=1,column=0)
    usr.insert(0,"Enter username")
    psw = Entry(root)
    psw.grid(row=2,column=0)
    psw.insert(0,"Enter password")
    win.title("chatApp -Login")

    def attempt_login():
        username = str(usr.get())
        password = str(psw.get())
        conn.login(username,password)
        go_to_home()

    def attempt_create():
        username = usr.get()
        password = psw.get()
        conn.create_user(username,password)
        go_to_home()
        
        
    
    confirmB = Button(root,text="Confirm",command=attempt_login)
    confirmB.grid(row=3,column=0)
    cancelB = Button(root,text="Cancel",command=go_to_home)
    cancelB.grid(row=4,column=0)
    createB = Button(root,text="Register",command=attempt_create)
    createB.grid(row=5,column=0)

def go_to_home():
    wipe_frame(groot)
    home(groot)


def content(root):
    for i in range(20):
        message = ' '
        if len(messages)>i:
            message = messages[i]
        elif i==0:
            message = "(NO MESSAGES)"
        m = Label(root, text=message)
        m.grid(row=1+i,column=3)
        
        
def message_send_screen(root):
    def send_message():
        chan = channelE.get()
        mess = messageE.get()
        conn.send_message(chan,mess)
        
        
        
        
    
    if acc:
        channelE = Entry(root)
        channelE.insert(0,"Channel")
        channelE.grid(row=21,column=2)
        messageE = Entry(root)
        messageE.insert(0,"Insert message here")
        messageE.grid(row=21,column=3)
        confirm = Button(root,text="Send",command=send_message)
        confirm.grid(row=22,column=2)
    


def home(root):
    def go_to_login():
        wipe_frame(root)
        login(root)

    homelabel = Label(root, text = "Home Screen")
    homelabel.grid(row=0,column=0)
    if acc == None:
        loginB = Button(root,text="Login",command=go_to_login)
        loginB.grid(row=2,column=0)
        win.title("chatApp -home (guest)")
    else:
        loginB = Button(root,text="Logout",command=logout)
        loginB.grid(row=2,column=0)
        channB = Button(root,text="join/create channel",command=join_create_channel)
        channB.grid(row=3,column=0)
        win.title("chatApp -home (user)")

    notif = Label(root, text = notification)
    notif.grid(row=5,column=0)
    content(root)
    message_send_screen(root)


    


def connection_screen():

    root = Frame(win)
    root.pack(side="top", expand=True, fill="both")
    
    instr = Label(root, text="connect to server:")
    ip_entry = Entry(root)
    ip_entry.insert(0,"Enter ip address")
    port_entry = Entry(root)
    port_entry.insert(0,"Enter port number")


    def confirmation_protocol():
        win.title("chatApp -establish connection")
        ip = ip_entry.get()
        port = port_entry.get()
        print("inputted ip:",ip,"port:",port)
        global conn
        conn = clientnet.ClientConnection()
        result = conn.connect(ip,port)
        if result != True:
            l = Label(root, text="Invalid attempt")
            l.grid(row=8)
        else:
            global groot
            groot = root
            wipe_frame(root)
            home(root)
            
            
    confirm = Button(root,text="Confirm", command=confirmation_protocol)

    instr.grid(row=0,column=0)
    ip_entry.grid(row=2,column=0)
    port_entry.grid(row=4,column=0)
    confirm.grid(row=6, column = 0)


if __name__ =='__main__':
        
    win.geometry("700x500")
    win.title("chatApp -establish connection")
    connection_screen()
    
    win.update()
    try:
        while win.state() == 'normal':
            win.update()
            
            if conn != None:
                conn.update()
                if conn.has_changed():
                    print("change detected in connection, updating")
                    for i in conn.get_messages():
                        interpret_input(i)
                    home(groot)
    except:
        print("has closed")
    conn.s.close()

