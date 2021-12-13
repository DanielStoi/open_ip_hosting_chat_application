# open_ip_hosting_chat_application
An application that allows people to run a chat server, and also connect to other people's server to communicate on different channels. Utilises python 3.9, generally only using build-in libraries. Everything was coded from scratch.

![demo home](https://github.com/DanielStoi/open_ip_hosting_chat_application/blob/main/demo/user%20home.PNG)

![demo home](https://github.com/DanielStoi/open_ip_hosting_chat_application/blob/main/demo/multiple_user_demo.PNG)
## setting up a server: 
servers are currently only accessable from localhost and LAN connections. A port forwarding rule needs to be set up on the router in order for the server to exist on the internet. 

run "server/server.py" and either specify the port and ip through the command line or though via inputs.

## setting up a client:
run "client/clientapp.py"

As long as a valid ip and port is provided, the client application is able to connect to any valid server (even through the internet).

Once a valid connection is established to a chat server, the user has the option of creating a user account (with a password and username), logging in and creating/joining channels to communicate through.
