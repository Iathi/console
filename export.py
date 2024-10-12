from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon import utils
import os, sys
import configparser
import csv
import time

print("\033[100mArquivo para Extrair Membros\033[m")

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"


cpass = configparser.RawConfigParser()
cpass.read('config.data')




with open('phone.csv', 'r') as f:
    str_list = [row[0] for row in csv.reader(f)]

    
    po = 0
    for pphone in str_list:
        
        
        phone = utils.parse_phone(pphone)
        po += 1
        
        
        print(f"Login {phone}")
        client = TelegramClient(f"sessions/{phone}", 2075988, '0d736429473d31199be9e61dc6afa2cd')
        time.sleep(1)
        try:
         client.start(phone)
        except:
         print("erro de sessao")
         
         

 
os.system('clear')
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
 
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
 
print(gr+'[+] Escolha o Grupo para Extrair Membros:'+re)
i=0
for g in groups:
    print(gr+'['+cy+str(i)+']' + ' - ' + g.title)
    i+=1
 
print('')
g_index = input(gr+"[+] Digite um Numero : "+re)
target_group=groups[int(g_index)]
 

time.sleep(1)
all_participants = []
all_participants = client.iter_participants(target_group, aggressive=True)
membros = 0
print(gr+'[+] Salvando')
time.sleep(1)
with open("members.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        membros = membros + 1
        time.sleep(0.04)
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])
        print(f"Usuarios Coletados {membros}\n") 
print(f"Numero de Membros Salvos {membros}")    
print(gr+'[+] Membros Extraidos')

