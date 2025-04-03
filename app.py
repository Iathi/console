from quart import Quart, render_template, request, redirect, url_for, session, jsonify
from telethon import TelegramClient
from telethon.sessions import StringSession
import os
import asyncio

# Inicialização do app
app = Quart(__name__)
app.secret_key = 'seu_segredo_aqui'

api_id = 24010179  # Substitua pelo seu API ID
api_hash = '7ddc83d894b896975083f985effffe11'  # Substitua pelo seu API Hash

client = None

# Função para garantir que a pasta 'sessions' exista
def ensure_sessions_dir():
    if not os.path.exists('sessions'):
        os.makedirs('sessions')

# Função assíncrona para iniciar o cliente Telegram
async def async_start_client(phone_number):
    global client
    ensure_sessions_dir()

    session_file = f'sessions/{phone_number}.session'
    
    if os.path.exists(session_file):
        with open(session_file, 'r') as f:
            session_string = f.read().strip()
            client = TelegramClient(StringSession(session_string), api_id, api_hash)
    else:
        client = TelegramClient(StringSession(), api_id, api_hash)
        await client.connect()

        if not await client.is_user_authorized():
            try:
                await client.send_code_request(phone_number)
                return {"status": "pending", "message": "Código enviado. Aguarde a inserção do código."}
            except Exception as e:
                return {"status": "error", "message": str(e)}

    await client.connect()
    return {"status": "success", "message": "Login bem-sucedido"}

# Rota para iniciar a sessão do usuário
@app.route('/login', methods=['POST'])
async def login():
    data = await request.get_json()
    phone_number = data.get('phone')

    if not phone_number:
        return jsonify({"status": "error", "message": "Número de telefone é obrigatório"}), 400

    result = await async_start_client(phone_number)
    return jsonify(result)

# Rota para inserir o código de verificação
@app.route('/verify', methods=['POST'])
async def verify():
    data = await request.get_json()
    phone_number = data.get('phone')
    code = data.get('code')

    if not phone_number or not code:
        return jsonify({"status": "error", "message": "Telefone e código são obrigatórios"}), 400

    global client
    try:
        await client.sign_in(phone_number, code)
        
        # Salvar a sessão
        session_string = client.session.save()
        session_file = f'sessions/{phone_number}.session'
        with open(session_file, 'w') as f:
            f.write(session_string)

        return jsonify({"status": "success", "message": "Sessão salva com sucesso!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# Rodar o aplicativo
if __name__ == '__main__':
    app.run(debug=True)
