import socket
import threading
import random
from random import randint
import string
from time import sleep
import tkinter
import tkinter.scrolledtext


class ChatClient:
    def __init__(self, host, port, nickname):
        self.host = host
        self.port = port
        self.nickname = nickname
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gui_done = False
        self.running = True

    def run_client(self):
        """Starting client"""
        # Connecting To Server
        self.client.connect((self.host, self.port))
        # Starting Threads For Listening And Writing
        gui_thread = threading.Thread(target=self._run_gui)
        gui_thread.start()

        receive_thread = threading.Thread(target=self._receive)
        receive_thread.start()

        # write_thread = threading.Thread(target=self._write)
        # write_thread.start()

        # simulation_thread = threading.Thread(target=self._simulate_chat)
        # simulation_thread.start()

    def _run_gui(self):
        """Creating GUI"""
        self.window = tkinter.Tk()

        # self.window.geometry('600x800')
        self.window.title('Chat Room')

        self.chat_label = tkinter.Label(self.window, text='Chat', font=('Arial', 24, 'bold'), padx=20, pady=10)
        self.chat_label.pack()

        self.text_area = tkinter.scrolledtext.ScrolledText(self.window, padx=20, pady=10, state='disabled')
        self.text_area.pack()

        self.message_label = tkinter.Label(self.window, text='Message', font=('Arial', 24, 'bold'), padx=20, pady=10)
        self.message_label.pack()

        self.entry = tkinter.Text(self.window, height=3, padx=20, pady=5)
        self.entry.pack()

        # self.entry = tkinter.Entry(self.window, font=('Arial', 12))
        # self.entry.pack()

        self.send_button = tkinter.Button(self.window,
                                          text='SEND',
                                          command=self._write,
                                          font=('Arial', 24),
                                          padx=20,
                                          pady=10)
        self.send_button.pack()

        self.gui_done = True

        self.window.protocol('WM_DELETE_WINDOW', self._stop)

        self.window.mainloop()

    def _stop(self):
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
        message = f'{self.nickname}: {self.entry.get("1.0", "end")}'
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
def chat_client(clients_number=1):
    for index in range(clients_number):
        ChatClient('127.0.0.1', 8081, f'nick_{str(index)}').run_client()


chat_client(2)
