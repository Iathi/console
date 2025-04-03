import asyncio
from telethon import TelegramClient

# Configuração do Bot
api_id = 24010179  # Substitua pelo seu API ID
api_hash = "7ddc83d894b896975083f985effffe11"  # Substitua pelo seu API Hash
bot_token = "7498558962:AAF0K2FbG1w8DlAWXvT9sPpPEZWe54LOYQ"  # Substitua pelo seu Token

# Inicializando o cliente
bot = TelegramClient("bot", api_id, api_hash)

async def start_console():
    await bot.connect()
    
    if not await bot.is_user_authorized():
        try:
            await bot.sign_in(bot_token=bot_token)
        except Exception as e:
            print(f"Erro ao autenticar: {e}")
            return

    print("Console do Telegram Bot iniciado. Digite comandos:")
    while True:
        cmd = input("> ")
        if cmd.lower() == "exit":
            print("Finalizando o bot...")
            break
        elif cmd.lower().startswith("send "):
            try:
                parts = cmd.split(" ", 2)
                user = parts[1]  # Número ou username do destinatário
                message = parts[2]  # Mensagem
                await bot.send_message(user, message)
                print(f"Mensagem enviada para {user}!")
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")
        else:
            print("Comando inválido. Use 'send <usuário> <mensagem>' ou 'exit' para sair.")

asyncio.run(start_console())
