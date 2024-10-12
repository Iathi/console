from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon import functions, types, TelegramClient, connection, sync, utils, errors
from telethon.errors import SessionPasswordNeededError
from telethon.errors.rpcerrorlist import UsernameInvalidError, ChannelInvalidError, PhoneNumberBannedError, YouBlockedUserError, PeerFloodError, UserRestrictedError, ChatWriteForbiddenError, UserAlreadyParticipantError, UserKickedError
import configparser
import os
import sys
import csv
import traceback
import time
import random
import pyfiglet
import random

gr="\033[1;32m"
cy="\033[1;36m"
banner = pyfiglet.figlet_format('Dark J')
banner2 = pyfiglet.figlet_format('Adder')
banner3 = pyfiglet.figlet_format('Gratis')
print(banner)
print(banner2)
print(banner3)
print("\033[100mScript Gratis Adicionador de Pessoas em Grupos do Telegram\033[m\n")

cpass = configparser.RawConfigParser()
cpass.read('config.data')

with open('phone.csv', 'r') as f:
    str_list = [row[0] for row in csv.reader(f)]

    
    po = 0
    for pphone in str_list:
        
        
        phone = utils.parse_phone(pphone)
        po += 1
        
        
        print(f"Logando Numero: {phone}")
        client = TelegramClient(f"sessions/{phone}", 2075988, '0d736429473d31199be9e61dc6afa2cd')
        time.sleep(1)
        try:
         client.start(phone)
        except:
         print("erro de sessao")

users = []
with open(r"members.csv", encoding='UTF-8') as f:  #Enter your file name
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print(gr+'Escolha o Grupo para Adicionar Membros:'+cy)
i = 0
for group in groups:
    print(str(i) + '- ' + group.title)
    i += 1

g_index = input("Digite o Numero do Grupo: ")
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

mode = int(input("Digite 1 para adicionar pelo Username ou 2 para adicionar pelo ID: "))

print("\nQuando Levar PeerFloodError ou FloodWaitError Mude de Numero em phone.csv")
time.sleep(1)
print("\nPara Continuar a adicionar a partir do usuario que parou procure no MTManager em members.csv a linha do nome usuario em Buscar e delete todas linhas anteriores até chegar na linha 2\n")
time.sleep(1)
n = 0
for user in users:
    n += 1
    if n % 50 == 0:
        time.sleep(10)
    try:
        print("\033[1;100mAdicionando {} no Grupo\033[m".format(user['name']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Numero Digitado Errado, Tente de Novo.")
        time.sleep(4)
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        time.sleep(4)
    except PeerFloodError:
        print("\n\033[1;41mPeerFloodError Vc Levou Spam do Telegram\033[m\n")
        sys.exit()
    except UserPrivacyRestrictedError:
        print("\033[1;31mUsuario nao Permite ser Adicionado\033[m")
        time.sleep(4)
    except UserAlreadyParticipantError:
        print("Usuario ja esta no Grupo")
        time.sleep(4)
    except errors.RPCError as e:
        status = e.__class__.__name__
        print(f'\033[1;31m{status}\033[m')
        if status == "FloodWaitError":
         print("\n\033[1;31mVoce Levou Flood do Telegram\033m\n")
         sys.exit()
        time.sleep(4)
        continue

