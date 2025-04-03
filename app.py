from telethon import TelegramClient, events
import re
import asyncio
import dns.resolver  

# Configurações do bot
api_id = 24010179  
api_hash = "7ddc83d894b896975083f985effffe11"
bot_token = "7498558962:AAF0K2FbIG1w8DlAWXvT9sPpPEZWe54LOYQ"

# Inicializando o bot corretamente
bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# Expressão regular para validar e-mail
email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

# ID do grupo
group_id = -4786957961

# Dicionário para rastrear usuários que precisam enviar um e-mail
users_restricted = {}

def save_email(user_name, email):
    """ Salva o e-mail válido em um arquivo txt """
    with open("emails.txt", "a", encoding="utf-8") as file:
        file.write(f"{user_name} - {email}\n")

def check_mx_record(email):
    """ Verifica se o e-mail tem um servidor de e-mail ativo """
    try:
        domain = email.split('@')[1]  
        mx_records = dns.resolver.resolve(domain, 'MX')  
        return bool(mx_records)
    except:
        return False  

@bot.on(events.ChatAction(chats=group_id))
async def new_member(event):
    """ Quando um usuário entra, pede o e-mail apenas uma vez """
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
    """ Verifica se o usuário enviou um e-mail válido, faz verificação real e apaga mensagens """
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
                await bot.send_message(user_id, "❌ O e-mail enviado não parece ser real. Envie um e-mail válido.")
        else:
            await event.delete()  
            await bot.send_message(user_id, "❌ Sua mensagem foi apagada. Envie um e-mail válido.")

print("Bot está rodando...")
bot.run_until_disconnected()
