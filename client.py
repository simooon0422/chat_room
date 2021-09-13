import socket
import threading
import random
from random import randint
import string
from time import sleep
import tkinter
import tkinter.scrolledtext


class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gui_done = False
        self.running = True

    def run_client(self):
        """Starting client"""
        # Connecting To Server
        self._run_login_gui()

        # Starting Threads
        receive_thread = threading.Thread(target=self._receive, daemon=True)
        receive_thread.start()

        # Starting Client GUI
        self._run_client_gui()

    def _run_login_gui(self):
        self.data_window = tkinter.Tk()

        self.data_window.geometry('250x350')

        # Specify Grid
        tkinter.Grid.columnconfigure(self.data_window, 0, weight=1)
        for i in range(8):
            tkinter.Grid.rowconfigure(self.data_window, i, weight=1)

        self.data_window.title('Chat Room')

        self.host_label = tkinter.Label(self.data_window, text='Host', font=('Arial', 12, 'bold'), padx=20, pady=10)
        self.host_label.grid(row=0, column=0, sticky="nsew", padx=40)
        self.host_entry = tkinter.Text(self.data_window, height=1, width=15)
        self.host_entry.insert('end', '127.0.0.1')
        self.host_entry.grid(row=1, column=0, sticky="nsew", padx=40)

        self.port_label = tkinter.Label(self.data_window, text='Port', font=('Arial', 12, 'bold'), padx=20, pady=10)
        self.port_label.grid(row=2, column=0, sticky="nsew", padx=40)
        self.port_entry = tkinter.Text(self.data_window, height=1, width=15)
        self.port_entry.insert('end', '8081')
        self.port_entry.grid(row=3, column=0, sticky="nsew", padx=40)

        self.nick_label = tkinter.Label(self.data_window, text='Nickname', font=('Arial', 12, 'bold'), padx=20, pady=10)
        self.nick_label.grid(row=4, column=0, sticky="nsew", padx=40)
        self.nick_entry = tkinter.Text(self.data_window, height=1, width=15)
        self.nick_entry.insert('end', 'nickname')
        self.nick_entry.grid(row=5, column=0, sticky="nsew", padx=40)

        self.connect_button = tkinter.Button(self.data_window,
                                             text='Connect',
                                             command=self._connect,
                                             font=('Arial', 18),
                                             )
        self.connect_button.grid(row=6, column=0, sticky="nsew", padx=40, pady=10)

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
            self.invalid_data_label.grid(row=7, column=0, sticky="nsew", padx=40)

    def _stop_login_gui(self):
        self.data_window.destroy()
        exit(0)

    def _run_client_gui(self):
        """Creating GUI"""
        self.window = tkinter.Tk()

        self.window.geometry('600x600')

        # Specify Grid
        tkinter.Grid.columnconfigure(self.window, 0, weight=1)
        for i in range(5):
            tkinter.Grid.rowconfigure(self.window, i, weight=1)

        self.window.title('Chat Room')

        self.chat_label = tkinter.Label(self.window, text='Chat', font=('Arial', 24, 'bold'), padx=20, pady=10)
        self.chat_label.grid(row=0, column=0, sticky="nsew", padx=40)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.window, padx=20, pady=10, state='disabled')
        self.text_area.grid(row=1, column=0, sticky="nsew", padx=40)

        self.message_label = tkinter.Label(self.window, text='Message', font=('Arial', 24, 'bold'), padx=20, pady=10)
        self.message_label.grid(row=2, column=0, sticky="nsew", padx=40)

        self.chat_entry = tkinter.Text(self.window, height=3, padx=20, pady=5)
        self.chat_entry.grid(row=3, column=0, sticky="nsew", padx=40)

        self.send_button = tkinter.Button(self.window,
                                          text='SEND',
                                          command=self._write,
                                          font=('Arial', 24),
                                          padx=20,
                                          pady=10)
        self.send_button.grid(row=4, column=0, sticky="nsew", padx=200, pady=20)

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
        message = f'{self.nickname}: {self.chat_entry.get("1.0", "end")}'.strip()
        self.client.send(message.encode())
        self.chat_entry.delete('1.0', 'end')

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


ChatClient().run_client()
