import socket
import threading
import random
from random import randint
import string
from time import sleep
import tkinter
import tkinter.scrolledtext
from tkinter import messagebox


class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gui_done = False
        self.running = True

    def run_client(self):
        """Starting client"""
        # Getting Data For Connection
        self._login_gui()
        # Connecting To Server
        # self.client.connect((self.host, self.port))

        # Starting Threads
        receive_thread = threading.Thread(target=self._receive, daemon=True)
        receive_thread.start()

        self._run_client_gui()

        # simulation_thread = threading.Thread(target=self._simulate_chat)
        # simulation_thread.start()

    def _login_gui(self):
        self.data_window = tkinter.Tk()

        self.data_window.geometry('200x300')

        self.data_window.title('Chat Room')

        self.host_label = tkinter.Label(self.data_window, text='Host', font=('Arial', 12, 'bold'), padx=20, pady=10)
        self.host_label.pack()
        self.host_entry = tkinter.Text(self.data_window, height=1, width=10, padx=20, pady=5)
        self.host_entry.insert('end', '127.0.0.1')
        self.host_entry.pack()

        self.port_label = tkinter.Label(self.data_window, text='Port', font=('Arial', 12, 'bold'), padx=20, pady=10)
        self.port_label.pack()
        self.port_entry = tkinter.Text(self.data_window, height=1, width=10, padx=20, pady=5)
        self.port_entry.insert('end', '8081')
        self.port_entry.pack()

        self.nick_label = tkinter.Label(self.data_window, text='Nickname', font=('Arial', 12, 'bold'), padx=20, pady=10)
        self.nick_label.pack()
        self.nick_entry = tkinter.Text(self.data_window, height=1, width=10, padx=20, pady=5)
        self.nick_entry.insert('end', 'nickname')
        self.nick_entry.pack()

        self.connect_button = tkinter.Button(self.data_window,
                                             text='Connect',
                                             command=self._connect,
                                             font=('Arial', 18),
                                             )
        self.connect_button.pack()

        self.invalid_data_label = tkinter.Label(self.data_window,
                                                text='Invalid Data',
                                                font=('Arial', 12, 'bold'),
                                                fg='red',
                                                padx=20,
                                                pady=10)

        self.data_window.protocol('WM_DELETE_WINDOW', self._stop_login_gui)

        self.data_window.mainloop()

    def _connect(self):
        try:
            self.host = self.host_entry.get('1.0', 'end').strip()
            self.port = int(self.port_entry.get('1.0', 'end'))
            self.nickname = self.nick_entry.get('1.0', 'end').strip()
            self.client.connect((self.host, self.port))
            self.data_window.destroy()
        except (ValueError, socket.gaierror):
            self.invalid_data_label.pack()

    def _stop_login_gui(self):
        self.data_window.destroy()
        exit(0)

    def _run_client_gui(self):
        """Creating GUI"""
        self.window = tkinter.Tk()

        self.window.title('Chat Room')

        self.chat_label = tkinter.Label(self.window, text='Chat', font=('Arial', 24, 'bold'), padx=20, pady=10)
        self.chat_label.pack()

        self.text_area = tkinter.scrolledtext.ScrolledText(self.window, padx=20, pady=10, state='disabled')
        self.text_area.pack()

        self.message_label = tkinter.Label(self.window, text='Message', font=('Arial', 24, 'bold'), padx=20, pady=10)
        self.message_label.pack()

        self.entry = tkinter.Text(self.window, height=3, padx=20, pady=5)
        self.entry.pack()

        self.send_button = tkinter.Button(self.window,
                                          text='SEND',
                                          command=self._write,
                                          font=('Arial', 24),
                                          padx=20,
                                          pady=10)
        self.send_button.pack()

        self.gui_done = True

        self.window.protocol('WM_DELETE_WINDOW', self._stop_client_gui)

        self.window.mainloop()

    def _stop_client_gui(self):
        """Stopping program"""
        self.running = False
        self.window.destroy()
        self.client.close()
        exit(0)

    def _receive(self):
        """Listening to Server and Sending Nickname"""
        while self.running:
            try:
                # Receive Message From Server
                # If 'NICK' Send Nickname
                message = self.client.recv(1024).decode()
                if message == 'NICK':
                    self.client.send(self.nickname.encode())
                elif self.gui_done:
                    self.text_area.config(state='normal')
                    self.text_area.insert('end', message)
                    self.text_area.yview('end')
                    self.text_area.config(state='disabled')
                    # print(message, end='')

            except:
                # Close Connection When Error
                print("An error occurred!")
                self.client.close()
                break

    def _write(self):
        """Writing messages"""
        message = f'{self.nickname}: {self.entry.get("1.0", "end")}'.strip()
        self.client.send(message.encode())
        self.entry.delete('1.0', 'end')

    def _simulate_chat(self):
        """Writing random messages"""
        while True:
            sleep(0.1)
            message = f'{self.nickname}: {self._get_random_string()}'
            self.client.send(message.encode())

    def _get_random_string(self):
        """Generating random string"""
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(randint(1, 20)))
        return str(result_str)


# ChatClient('127.0.0.1', 8081, 'nick').run_client()
# def chat_client(clients_number=1):
#     for index in range(clients_number):
#         ChatClient('127.0.0.1', 8081, f'nick_{str(index)}').run_client()


# chat_client()
ChatClient().run_client()
