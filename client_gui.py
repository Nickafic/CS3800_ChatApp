#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import ssl

SERVER_IP = 'localhost'
PORT = 12345
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'

# Create an SSL context
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Initialize socket
client = socket(AF_INET, SOCK_STREAM)

# Wrap the socket with SSL
ssl_client = context.wrap_socket(client, server_hostname=SERVER_IP)
ssl_client.connect(ADDR)

print("Choose your nickname")
nickname = input("")

# Send the nickname as the first message to the server
ssl_client.send(nickname.encode(FORMAT))

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = ssl_client.recv(1024).decode(FORMAT)
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break

def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    if msg == "{quit}":
        ssl_client.send("{quit}".encode(FORMAT))  # Send quit message to server to initiate closing
        ssl_client.close()
        top.quit()
    else:
        ssl_client.send(msg.encode(FORMAT))  # Send only the message

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

# GUI layout
top = tkinter.Tk()
top.title("Chat")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

receive_thread = Thread(target=receive, daemon=True)
receive_thread.start()

tkinter.mainloop()
