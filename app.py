from telethon import TelegramClient
import os

# Pegando as variáveis de ambiente no Railway
api_id = int(os.getenv("API_ID", "24010179"))
api_hash = os.getenv("API_HASH", "7ddc83d894b896975083f985effffe11")
bot_token = os.getenv("BOT_TOKEN", "7498558962:AAF0K2FbG1w8DlAWXvT9sPpPEZWe54LOYQ")

# Criar o cliente e salvar a sessão no arquivo "bot.session"
bot = TelegramClient("bot.session", api_id, api_hash)

async def main():
    await bot.connect()

    if not await bot.is_user_authorized():
        print("🔑 Autenticando com o bot token...")
        await bot.start(bot_token=bot_token)

    print("🤖 Bot iniciado e sessão salva!")
    await bot.run_until_disconnected()

# Iniciar o bot sem pedir input
bot.loop.run_until_complete(main())
