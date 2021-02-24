"""D."""
# import getpass
# import io
import json
import os
import select
import sys
import threading
from multiprocessing import Process
import time
import unittest
import random
import re

import vk_api
from requests import exceptions
from vk_api import bot_longpoll
# import ancet
# import keyboards
from datetime import date
import calendar
import json
from google.oauth2 import service_account
# import pys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
import pygsheets
import vk_api
import keyboards

scheduleUrl = 'https://docs.google.com/spreadsheets/d/1Da9tacWq4DvCVQjKJtkA4-ZlkqyFrntO0sW4Yrxsl3A/edit?usp=sharing'
recsUrl = "https://docs.google.com/spreadsheets/d/1Da9tacWq4DvCVQjKJtkA4-ZlkqyFrntO0sW4Yrxsl3A/edit#gid=698023837"
tableId = "1Da9tacWq4DvCVQjKJtkA4-ZlkqyFrntO0sW4Yrxsl3A"

client = pygsheets.authorize(service_file='./MasterShool-6008de092354.json')
# client = pygsheets.authorize()
# b = client.open_by_url(recsUrl)
# n = b[1][1]
a= client.open_by_url(scheduleUrl)
schedule = a[0]
recs = a[1]
# print(wk1)
b=0
# for i in range(wk1.r)
max_row = 0
a = schedule.get_col(1)
a = schedule.get_value((2, 5))
for i in a:
    if a == '':
       pass 
a = schedule.rows
a= schedule.get_values(start='A1', end=f'A{schedule.rows}')
a = schedule.get_col(1, include_tailing_empty=False)
# b = schedule.cell[1][1]
# df = pygsheets.DataRange()
# df.dropna(subset=['Volume'], inplace=True)


def get_empty_gaps():
    for row in range(2, schedule.rows):
        for col in range(0, schedule.cols):
            a = schedule[row][col]
            a = 0

# get_empty_gaps()
my_id = 160500068
groupid = 138409844

authed = False

global clients
clients = {}

command = ''
main_session = None
session = None
running_menu = True
vk = None

max_col = len(schedule.get_row(1, include_tailing_empty=False))
max_row = len(schedule.get_col(1, include_tailing_empty=False))
rec_max_col = len(recs.get_row(1, include_tailing_empty=False))
rec_max_row = len(recs.get_col(1, include_tailing_empty=False))

v = schedule.get_values(start=(1,1), end=(max_row, max_col))
class Anceteur():

    def __init__(self):
        self.authed = False
        self.longpollServer = None
        self.cup = 1
        self.token = open('./token.cfg', 'r').readline().replace('\n', '')
        self.currentAncetOnVoting = None
        self.idToInvite = None
        self.ancetsToSendStack = []

    def auth(self):
        """Authentificate bot as group."""
        try:
            print("You are going to log in as Полигон")
            # os.system('clear')
            self.session = vk_api.VkApi(token=self.token)
            self.session._auth_token()
            print("authred")
            vk = self.session.get_api()
            global authed
            self.authed = True
            self.longpollserver = bot_longpoll.VkBotLongPoll(self.session, 138409844)
            self.gLPS = threading.Thread(target=self.lps, args=(self.session, ), daemon=True)
            # self.gLPS.start()
            print('gAut Online')
            self.lps(session = self.session)
            return True
        except Exception as e:
            print(e)
            pass


    def lps(self, session):
        for event in bot_longpoll.VkBotLongPoll.listen(self.longpollserver):
            payload = event.raw.get("object").get("payload")
            sender_id = event.raw.get("object").get("from_id")
            msg_text = event.raw.get("object").get("text")
            if sender_id not in clients.keys():
                clients.update({sender_id: {}})
            dates = {}
            data = self.session.method("users.get", {"user_ids":sender_id, "fields": "domain"})[0]
            val = f"{data['first_name']} {data['last_name']}"
            link = f"https://vk.com/{data['domain']}"
            vals = schedule.get_values(start=(1,1), end=(max_row, max_col), include_tailing_empty=True) 
            tmp = []
            for i in vals:
                for j in i:
                    tmp.append(j)
            if ("записаться" in event.raw.get("object").get("text").lower() or payload == '{\"command\":\"start\"}' or event.raw.get("object").get("text").lower() == 'd'):
                if val not in tmp:
                    msg = "Доступны даты:\n"
                    aa = schedule.get_col(1, include_tailing_empty=False)[1:]
                    for i,j in enumerate(list(map(lambda x: x[0], vals[1:]))):
                        i += 1
                        z = vals[i][0]
                        msg += f"{len(dates) + 1} : {z}\n"
                        dates.update({f"{len(dates)+1}": (i, 0)})
                        pass
                    clients.update({sender_id: [dates, 1]})
                    self.Dialog(sender_id, "Этот бот поможет зарегистрироваться на собеседование\nСобеседование будет проходить в нашем офисе, который расположен недалеко от метро Сокол, по адресу Волоколамское шоссе, 1кА.\nПодробнее можно посмотреть по ссылке.\nhttps://drujite.ru/contacts/")
                    self.Dialog(sender_id, msg,keybaord=keyboards.confKB)
                else: 
                    self.Dialog(sender_id, "Вы уже записаны", keybaord= keyboards.undoKB)
            
            elif msg_text.lower() == "отменить" or payload == '{\"mainMenu\":\"undo\"}':

                if val in tmp:
                    msg = "Доступны даты:\n"
                    aa = schedule.get_col(1, include_tailing_empty=False)[1:]
                    b = list(map(lambda x: x[0], vals[1:]))
                    for i,j in enumerate(list(map(lambda x: x[0], vals[1:]))):
                        i += 1
                        z = vals[i][1:max_col]
                        for index, val in enumerate(z):
                            if val == f"{data['first_name']} {data['last_name']}":
                                сell = schedule.cell((i + 1,index +2))
                                schedule.cell((i + 1,index +2)).value = ""
                                schedule.cell((i + 1,index +2)).color = (1,1,1,1)
                                break
                    clients.update({sender_id: dates})
                    self.Dialog(sender_id, "Запись отменена. Вы можете записаться на новую дату", keybaord=keyboards.beginKb)
                pass

            elif payload == '{\"mainMenu\":\"fuck_go_back\"}':
                if val not in tmp:
                    msg = "Доступны даты:\n"
                    aa = schedule.get_col(1, include_tailing_empty=False)[1:]
                    for i,j in enumerate(list(map(lambda x: x[0], vals[1:]))):
                        i += 1
                        z = vals[i][0]
                        msg += f"{len(dates) + 1} : {z}\n"
                        dates.update({f"{len(dates)+1}": (i, 0)})
                        pass
                    clients.update({sender_id: [dates, 1]})
                    self.Dialog(sender_id, msg,keybaord=keyboards.confKB)
                else: 
                    self.Dialog(sender_id, "Вы уже записаны", keybaord=keyboards.undoKB)
            elif payload == '{\"mainMenu\":\"new_date\"}':
                self.Dialog(sender_id, "Напишите даты и промежутки времени, в которое вы могли бы приехать на собеседование")
                clients.update({sender_id: None})
                pass

            else:
                if sender_id in clients.keys() and clients[sender_id] != {}:
                    a = clients[sender_id]
                    if clients[sender_id] is None:
                        a = rec_max_col
                        b = rec_max_row
                        c = recs.cell((b+1, 1))
                        c.value = msg_text
                        c = recs.cell((b+1, 2))
                        c.value = f'=HYPERLINK(\"{link}\"; \"{val}\")'
                        recs.adjust_column_width(2)
                        recs.adjust_column_width(1)
                        self.Dialog(sender_id, "Заявка на собеседование отправлена. С вами свяжутся")
                        clients.pop(sender_id)
                        pass
                    elif clients[sender_id][1] == 1:
                        if msg_text in clients[sender_id][0].keys():
                            if val not in tmp:
                                msg = "Доступны даты:\n"
                                aa = schedule.get_col(1, include_tailing_empty=False)[1:]
                                i = clients[sender_id][0][msg_text][0]
                                z = vals[i][1:max_col]
                                for index, val in enumerate(z):
                                    if val == "":
                                        dates.update({f"{len(dates)+1}": (i +1, index +2)})
                                        msg += f"{len(dates)} - записаться на {vals[i][0]} в {vals[0][index+1]}\n"
                                        pass
                                pass
                                clients.update({sender_id: [dates, 2]})
                                self.Dialog(sender_id, msg,keybaord=keyboards.fuck_go_backKB)
                    elif clients[sender_id][1] == 2:
                        self.Dialog(sender_id, "Обращение к базе данных может занять некоторое время...")
                        if msg_text in clients[sender_id][0].keys():
                            a= clients[sender_id][0][msg_text]
                            cell = schedule.cell(a)
                            if cell.value == '':
                                cell.formula = f'=HYPERLINK(\"{link}\"; \"{val}\")'
                                schedule.adjust_column_width(a[1])
                                cell.color = (0,1,0,1)
                                clients.pop(sender_id)
                                
                                self.Dialog(usrId = sender_id, message = "Вы успешно записаны!\nЧтобы отменить запись, нажмите на соответствующую кнопку или введите 'Отменить'")
                                self.Dialog(sender_id, "Собеседование будет проходить в нашем офисе, который расположен недалеко от метро Сокол, по адресу Волоколамское шоссе, 1кА.\nПодробнее можно посмотреть по ссылке.\nhttps://drujite.ru/contacts/", keybaord=keyboards.undoKB)
                            else:
                                self.Dialog(usrId = sender_id, message = "Упс, кто-то успел записаться раньше, обновляем список.")
                                if val not in tmp:
                                    msg = "Доступны даты:\n"
                                    aa = schedule.get_col(1, include_tailing_empty=False)[1:]
                                    for i,j in enumerate(list(map(lambda x: x[0], vals[1:]))):
                                        i += 1
                                        z = vals[i][0]
                                        msg += f"{len(dates) + 1} : {z}\n"
                                        dates.update({f"{len(dates)+1}": (i, 0)})
                                        pass
                                    clients.update({sender_id: [dates, 1]})
                                    self.Dialog(sender_id, msg,keybaord=keyboards.confKB)
                                else: 
                                    self.Dialog(sender_id, "Вы уже записаны", keybaord= keyboards.undoKB)
                                pass
                            pass
                    pass
                
                else:
                    self.Dialog(sender_id, "Этот бот поможет зарегистрироваться на собеседование\nСобеседование будет проходить в нашем офисе, который расположен недалеко от метро Сокол, по адресу Волоколамское шоссе, 1кА.\nПодробнее можно посмотреть по ссылке.\nhttps://drujite.ru/contacts/", keybaord=keyboards.beginKb)
                    pass
            time.sleep(0.1)

    def Dialog(self, usrId: int, message: str, keybaord=None):
        r"""
        Dialog is method to send messges to users.
        usrId: Id to send message
        messge: message to send
        keyboard(not obligatory): keyboard from \'keyboards\' module
        """
        if keybaord:
            self.session.method("messages.send",
                                                {
                                                    "peer_id": usrId,
                                                    "keyboard": keybaord,
                                                    "random_id" : random.randint(1, 10000000000),
                                                    "message": message
                                                })
        else:
            self.session.method("messages.send",
                                                {
                                                    "peer_id": usrId,
                                                    "random_id" : random.randint(1, 10000000000),
                                                    "message": message
                                                })

while True:
    a = Anceteur()
    a.auth()
