from flask import Flask, request, jsonify
from telethon import TelegramClient
import asyncio

app = Flask(__name__)

# Substitua pelos seus valores do Telegram
API_ID = 24010179  # Seu API_ID do Telegram
API_HASH = "7ddc83d894b896975083f985effffe11"  # Seu API_HASH do Telegram

# Variável global para armazenar o cliente
bot_client = None

@app.route("/connect-bot", methods=["POST"])
def connect_bot():
    global bot_client

    try:
        data = request.json
        bot_token = data.get("bot_token")

        if not bot_token:
            return jsonify({"success": False, "error": "Token não fornecido!"})

        # Criando o cliente do Telethon
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        bot_client = TelegramClient("bot", API_ID, API_HASH)
        loop.run_until_complete(bot_client.start(bot_token=bot_token))

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
