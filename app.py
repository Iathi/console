import os
import re
import asyncio
import dns.resolver  # Para verificar se o e-mail tem servidor ativo
from telethon import TelegramClient, events

# Configurações do bot (usando variáveis de ambiente)
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
group_id = int(os.getenv("GROUP_ID"))

# Inicializando o bot
bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# Expressão regular para validar e-mails
email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

# Dicionário para rastrear usuários que precisam enviar um e-mail
users_restricted = {}

def save_email(user_name, email):
    """Salva o e-mail válido em um arquivo txt"""
    with open("emails.txt", "a", encoding="utf-8") as file:
        file.write(f"{user_name} - {email}\n")

def check_mx_record(email):
    """Verifica se o e-mail tem um servidor de e-mail ativo"""
    try:
        domain = email.split('@')[1]
        mx_records = dns.resolver.resolve(domain, 'MX')
        return bool(mx_records)
    except:
        return False

@bot.on(events.ChatAction(chats=group_id))
async def new_member(event):
    """Quando um usuário entra, pede o e-mail apenas uma vez"""
    if event.user_joined or event.user_added:
        user_id = event.user_id
        if user_id not in users_restricted:
            users_restricted[user_id] = True
            welcome_message = (
                f"👋 Bem-vindo {event.user.first_name}! Envie um e-mail válido para liberar seu acesso ao grupo.\n\n"
                "🔹 O que você encontra no grupo?\n"
                "✅ Automação para Facebook, Instagram, Telegram e WhatsApp\n"
                "✅ Suporte técnico e dicas\n"
                "✅ Novidades sobre ferramentas de automação\n"
                "✅ Troca de experiências com outros usuários\n\n"
                "🚀 Teste grátis! Acesse: https://bio.site/AutoCommenterPro."
            )
            await bot.send_message(group_id, welcome_message)

@bot.on(events.NewMessage(chats=group_id))
async def check_email(event):
    """Verifica se o usuário enviou um e-mail válido e faz a verificação real"""
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

print("Bot está rodando...")
bot.run_until_disconnected()
