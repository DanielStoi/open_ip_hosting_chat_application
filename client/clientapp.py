from tkinter import *
import clientnet
win = Tk()
acc = None #account if logged in
conn = None #network connection to server
messages = list()
MAX_MESSAGES = 20
groot = None

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
            message = "USER: "+message[0]+" CHANNEL:"+ message[1]+"\tSEND: " +" ".join(message[2:])
            messages.append(message)
        else:
            messages.append(" ".join(message))

        if len(messages)>MAX_MESSAGES:
            messages.pop(0)
    else:
        print("cannot inperpret:",s)



        

def wipe_frame(frame):
    for item in frame.winfo_children():
      item.destroy()
########
#ROUTES
########




########
#Connection screen
########



            
    


def logout():
    
    global acc
    acc = None
    conn.logout()
    home(groot)

def login(root):
    instr = Label(root, text="login to account")
    instr.grid(row=0,column=0)
    usr = Entry(root)
    usr.insert(0,"Enter username")
    usr.grid(row=1,column=0)
    psw = Entry(root)
    psw.insert(0,"Enter password")
    psw.grid(row=2,column=0)
    win.title("chatApp -Login")

    def attempt_login():
        username = usr.get()
        password = psw.get()
        conn.login(usr,psw)
        go_to_home()
    
    confirmB = Button(root,text="Confirm",command=attempt_login)
    confirmB.grid(row=3,column=0)
    cancelB = Button(root,text="Cancel",command=go_to_home)
    cancelB.grid(row=4,column=0)

def go_to_home():
    wipe_frame(groot)
    home(groot)


def content(root):
    if len(messages) == 0:
        m = Label(root, text="(NO MESSAGES)")
        m.grid(row=1,column=3)
        return
    for i in range(20):
        message = ' '
        if len(messages)>i:
            message = messages[i]
        m = Label(root, text=message)
        m.grid(row=1+i,column=3)
        
        
def message_send_screen(root):
    if acc:
        channelE = Entry(root)
        channelE.insert(0,"Channel")
        channelE.grid(row=21,column=2)
        messageE = Entry(root)
        messageE.insert(0,"Insert message here")
        messageE.grid(row=21,column=3)
        confirm = Button(root,text="Send")
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
        channB = Button(root,text="Join a Channel",command=logout)
        channB.grid(row=3,column=0)
        win.title("chatApp -home (user)")


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
    
    print("26")
    while True: 
        win.update()
        
        if conn != None:
            conn.update()
            if conn.has_changed():
                print("change detected in connection, updating")
                for i in conn.get_messages():
                    interpret_input(i)
                home(groot)


