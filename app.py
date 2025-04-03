from quart import Quart, render_template, request, redirect, url_for, session, jsonify
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os
import asyncio
import re
import dns.resolver  # Para verificar MX de e-mail

app = Quart(__name__)
app.secret_key = 'seu_segredo_aqui'

api_id = 24010179
api_hash = "7ddc83d894b896975083f985effffe11"
bot_token = "7498558962:AAF0K2FbG1w8DlAWXvT9sPpPEZWe54LOYQ"

# Configuração do Telegram Client
bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# Grupo alvo
group_id = -1002222583428
users_restricted = {}
email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+"

async def check_mx_record(email):
    """Verifica se o e-mail tem um servidor ativo"""
    try:
        domain = email.split('@')[1]
        mx_records = dns.resolver.resolve(domain, 'MX')
        return bool(mx_records)
    except:
        return False

def save_email(user_name, email):
    """Salva e-mail válido"""
    with open("emails.txt", "a", encoding="utf-8") as file:
        file.write(f"{user_name} - {email}\n")

@bot.on(events.ChatAction(chats=group_id))
async def new_member(event):
    """Recebe novos usuários"""
    if event.user_joined or event.user_added:
        user_id = event.user_id
        if user_id not in users_restricted:
            users_restricted[user_id] = True
            welcome_message = """
                👋 Bem-vindo! Envie um e-mail válido para liberar seu acesso.
            """
            await bot.send_message(group_id, welcome_message)

@bot.on(events.NewMessage(chats=group_id))
async def check_email(event):
    """Verifica e-mails e libera usuários"""
    user_id = event.sender_id
    message_text = event.raw_text
    
    if user_id in users_restricted:
        match = re.search(email_regex, message_text)
        if match:
            email = match.group()
            if await check_mx_record(email):
                save_email(event.sender.first_name, email)
                await event.delete()
                del users_restricted[user_id]
                await bot.send_message(group_id, f"✅ Obrigado, {event.sender.first_name}! Acesso liberado.")
            else:
                await event.delete()
                await bot.send_message(user_id, "❌ E-mail inválido. Envie um correto.")
        else:
            await event.delete()
            await bot.send_message(user_id, "❌ Mensagem apagada. Envie um e-mail válido.")

@app.before_serving
async def startup():
    """Inicia o bot ao iniciar o servidor"""
    asyncio.create_task(bot.run_until_disconnected())

@app.route('/')
async def index():
    return "Bot e servidor rodando!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
