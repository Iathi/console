from telethon import TelegramClient, events
import os

# Configurações do bot
api_id = 24010179  
api_hash = "7ddc83d894b896975083f985effffe11"
bot_token = "7498558962:AAF0K2FbG1w8DlAWXvT9sPpPEZWe54LOYQ"

# Criar e salvar sessão
session_name = "bot_session"  # Nome do arquivo de sessão
bot = TelegramClient(session_name, api_id, api_hash)

async def main():
    await bot.start(bot_token=bot_token)
    print("Bot iniciado e sessão salva!")

# Iniciar o bot
with bot:
    bot.loop.run_until_complete(main())
    bot.run_until_disconnected()
