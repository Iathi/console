from telethon import TelegramClient
import os

# Pegando as variáveis de ambiente do Railway (se não existirem, use os valores fixos)
api_id = int(os.getenv("API_ID", 24010179))
api_hash = os.getenv("API_HASH", "7ddc83d894b896975083f985effffe11")
bot_token = os.getenv("BOT_TOKEN", "7498558962:AAF0K2FbG1w8DlAWXvT9sPpPEZWe54LOYQ")

# Criar e salvar sessão no arquivo "bot.session"
bot = TelegramClient("bot", api_id, api_hash)

async def main():
    await bot.start(bot_token=bot_token)  # Não pede input manual!
    print("🤖 Bot iniciado e sessão salva!")
    await bot.run_until_disconnected()

# Iniciar o bot
with bot:
    bot.loop.run_until_complete(main())
