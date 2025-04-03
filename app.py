from flask import Flask, request, jsonify
from telethon import TelegramClient
import asyncio

app = Flask(__name__)

# Configuração do Telegram API
API_ID = 24010179  # Substitua pelo seu API_ID
API_HASH = "7ddc83d894b896975083f985effffe11"  # Substitua pelo seu API_HASH

bot_client = None  # Variável para armazenar o cliente do bot

@app.route("/connect-bot", methods=["POST"])
def connect_bot():
    global bot_client

    data = request.json
    bot_token = data.get("bot_token")

    if not bot_token:
        return jsonify({"success": False, "error": "Token do bot não foi fornecido!"})

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        bot_client = TelegramClient("bot", API_ID, API_HASH)
        loop.run_until_complete(bot_client.start(bot_token=bot_token))

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
