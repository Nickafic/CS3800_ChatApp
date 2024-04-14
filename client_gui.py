#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

SERVER_IP = 'localhost'  # Server's IP address
PORT = 12345
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket(AF_INET, SOCK_STREAM)
client.connect(ADDR)

print("Choose your nickname")
nickname = f'{input("")}'

def receive():
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            list.insert(tkinter.END, msg)
        except:
            print("An error occurred!")
            break


def write(event = None):
    msg = my_message.get()
    message = f'{nickname}: {msg}'
    my_message.set("")
    client.send(bytes(message, FORMAT))

    if msg == "{quit}":
        client.close()
        top.quit()


def on_closing(event = None):
    my_message.set("{quit}")
    write()

# user interface
top = tkinter.Tk()
top.title("Chat")

frame = tkinter.Frame(top)
my_message = tkinter.StringVar()
scrollbar = tkinter.Scrollbar(frame)

list = tkinter.Listbox(frame, height = 20, width = 50, yscrollcommand = scrollbar.set)
scrollbar.pack(side = tkinter.RIGHT, fill = tkinter.Y)
list.pack(side = tkinter.LEFT, fill = tkinter.BOTH)
frame.pack()

entry_field = tkinter.Entry(top, textvariable = my_message)
entry_field.bind("<Return>", write )
entry_field.pack()
send_button = tkinter.Button(top, text = "Send", command = write)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

receive_thread = Thread(target = receive)
receive_thread.start()

tkinter.mainloop()