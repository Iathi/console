from quart import Quart, request, redirect, url_for, session, jsonify
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os
import asyncio
import re
import dns.resolver

# Configurações do bot
api_id = 24010179
api_hash = "7ddc83d894b896975083f985effffe11"
bot_token = "7498558962:AAF0K2FbG1w8DlAWXvT9sPpPEZWe54LOYQ"
group_id = -1002222583428

# Inicialização do bot
bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# Expressão regular para validar e-mail
email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+"

# Dicionário para rastrear usuários
users_restricted = {}

# Inicialização do app Quart
app = Quart(__name__)
app.secret_key = 'seu_segredo_aqui'

def ensure_sessions_dir():
    if not os.path.exists('sessions'):
        os.makedirs('sessions')

def save_email(user_name, email):
    with open("emails.txt", "a", encoding="utf-8") as file:
        file.write(f"{user_name} - {email}\n")

def check_mx_record(email):
    try:
        domain = email.split('@')[1]
        mx_records = dns.resolver.resolve(domain, 'MX')
        return bool(mx_records)
    except:
        return False

@bot.on(events.ChatAction(chats=group_id))
async def new_member(event):
    if event.user_joined or event.user_added:
        user_id = event.user_id
        if user_id not in users_restricted:
            users_restricted[user_id] = True
            welcome_message = (
                f"👋 Bem-vindo {event.user.first_name}! Envie um e-mail válido para liberar seu acesso ao grupo."
            )
            await bot.send_message(group_id, welcome_message)

@bot.on(events.NewMessage(chats=group_id))
async def check_email(event):
    user_id = event.sender_id
    message_text = event.raw_text
    
    if user_id in users_restricted:
        match = re.search(email_regex, message_text)
        if match:
            email = match.group()
            if check_mx_record(email):
                save_email(event.sender.first_name, email)
                await asyncio.sleep(2)
                await event.delete()
                del users_restricted[user_id]
                await bot.send_message(group_id, f"✅ Obrigado, {event.sender.first_name}! Seu acesso ao grupo foi liberado.")
            else:
                await event.delete()
                await bot.send_message(user_id, "❌ O e-mail enviado não parece ser real. Envie um e-mail válido para continuar.")
        else:
            await event.delete()
            await bot.send_message(user_id, "❌ Sua mensagem foi apagada. Envie um e-mail válido para continuar no grupo.")

@app.route('/')
async def index():
    return "Bot está rodando!"

if __name__ == '__main__':
    print("Bot está rodando...")
    loop = asyncio.get_event_loop()
    loop.create_task(bot.run_until_disconnected())
    app.run(debug=True, port=5000)
