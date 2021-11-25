from tkinter import *
import clientnet
win = Tk()

conn = None
#####
#Connection screen
#####


def wipe_frame(frame):
    for item in frame.winfo_children():
      item.destroy()
    

def login(root):
    
    instr = Label(root, text="login to account")
    instr.grid(row=0,column=0)
    usr = Entry(root)
    usr.insert(0,"Enter username")
    usr.grid(row=1,column=0)
    psw = Entry(root)
    psw.insert(0,"Enter password")
    psw.grid(row=2,column=0)
    confirmB = Button(root,text="Confirm")
    confirmB.grid(row=3,column=0)
    cancelB = Button(root,text="Cancel")
    cancelB.grid(row=4,column=0)
    

def home(root):
    def go_to_login():
        wipe_frame(root)
        login(root)
    

    homelabel = Label(root, text = "Home Screen")
    homelabel.grid(row=0,column=0)
    loginB = Button(root,text="Login",command=go_to_login)
    loginB.grid(row=2,column=0)
    


def connection_screen():

    root = Frame(win)
    root.pack(side="top", expand=True, fill="both")
    
    instr = Label(root, text="connect to server:")
    ip_entry = Entry(root)
    ip_entry.insert(0,"Enter ip address")
    port_entry = Entry(root)
    port_entry.insert(0,"Enter port number")


    def confirmation_protocol():
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
            wipe_frame(root)
            home(root)
            
            
            
        
        
    
    confirm = Button(root,text="Confirm", command=confirmation_protocol)

    instr.grid(row=0,column=0)
    ip_entry.grid(row=2,column=0)
    port_entry.grid(row=4,column=0)
    confirm.grid(row=6, column = 0)


if __name__ =='__main__':
        
    win.geometry("700x500")
    connection_screen()
    
    print("26")
    win.mainloop()
    print("25")


