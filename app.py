from quart import Quart, render_template, request, redirect, url_for, session, jsonify, flash
from telethon import TelegramClient
from telethon.sessions import StringSession
import os
import asyncio
import subprocess

app = Quart(__name__)
app.secret_key = 'seu_segredo_aqui'  # O segredo é necessário para usar sessões e flash

# API ID e Hash
api_id = '24010179'  # Substitua pelo seu API ID
api_hash = '7ddc83d894b896975083f985effffe11'  # Substitua pelo seu API Hash

client = None
sending = False  # Variável global para controlar o envio
stop_sending_event = asyncio.Event()

# Função para garantir que o diretório de sessões exista
def ensure_sessions_dir():
    if not os.path.exists('sessions'):
        os.makedirs('sessions')

# Função assíncrona para inicializar o cliente
async def async_start_client(phone_number):
    global client
    session_file = f'sessions/{phone_number}.session'
    ensure_sessions_dir()
    
    if os.path.exists(session_file):
        with open(session_file, 'r') as f:
            session_string = f.read().strip()
            client = TelegramClient(StringSession(session_string), api_id, api_hash)
    else:
        client = TelegramClient(StringSession(), api_id, api_hash)
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)
            return False  # Necessário verificar o código
        session_string = client.session.save()
        with open(session_file, 'w') as f:
            f.write(session_string)
    
    await client.connect()
    return True  # Login bem-sucedido

# Página de login
@app.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':
        phone_number = (await request.form)['phone_number']
        session['phone_number'] = phone_number
        if not await async_start_client(phone_number):
            flash('Código de verificação enviado! Verifique seu telefone.', 'info')
            return redirect(url_for('verify_code'))
        flash('Login bem-sucedido!', 'success')
        return redirect(url_for('index'))
    return await render_template('login.html')

# Verificação de código após o login
@app.route('/verify_code', methods=['GET', 'POST'])
async def verify_code():
    if request.method == 'POST':
        code = (await request.form)['code']
        phone_number = session.get('phone_number')
        if client and client.session:
            try:
                await client.sign_in(code=code)
                # Após a verificação, salve a sessão
                session_file = f'sessions/{phone_number}.session'
                session_string = client.session.save()
                with open(session_file, 'w') as f:
                    f.write(session_string)
                flash('Verificação bem-sucedida! Você está logado.', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f"Erro ao verificar o código: {e}", 'danger')
    return await render_template('verify_code.html')

# Página inicial
@app.route('/')
async def index():
    if 'phone_number' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))

    phone_number = session.get('phone_number')

    if client is None or not client.is_connected():
        await async_start_client(phone_number)

    try:
        dialogs = await client.get_dialogs()
        groups = [(dialog.id, dialog.name) for dialog in dialogs if dialog.is_group]
        return await render_template('index.html', groups=groups)
    except Exception as e:
        flash(f"Erro ao tentar listar os grupos: {str(e)}", 'danger')
        return await render_template('index.html', groups=[])

# Envio de mensagens
@app.route('/send_messages', methods=['POST'])
async def send_messages():
    global sending, stop_sending_event
    form = await request.form
    group_ids = form.getlist('groups')
    delay = float(form['delay'])
    message = form['message']

    session['status'] = {'sending': [], 'errors': []}
    sending = True
    stop_sending_event.clear()

    async def send_messages_task():
        global sending
        for group_id in group_ids:
            if not sending:
                break
            try:
                await client.send_message(int(group_id), message)
                session['status']['sending'].append(f"✅ Mensagem enviada para o grupo {group_id}")
                await asyncio.sleep(delay)
            except Exception as e:
                session['status']['errors'].append(f"❌ Erro ao enviar mensagem para o grupo {group_id}: {str(e)}")

        sending = False
        stop_sending_event.set()

    await send_messages_task()
    flash('Mensagens enviadas!', 'success')
    return jsonify(session['status'])

# Verificação de status
@app.route('/status_updates')
async def status_updates():
    if 'status' in session:
        return jsonify(session['status'])
    return jsonify({'sending': [], 'errors': []})

# Parar o envio de mensagens
@app.route('/stop_sending', methods=['POST'])
async def stop_sending():
    global sending
    sending = False
    stop_sending_event.set()
    flash('Envio de mensagens interrompido.', 'warning')
    return jsonify(session.get('status', {'sending': [], 'errors': []}))

# Execução de comandos do terminal
@app.route('/execute', methods=['POST'])
async def execute():
    command = (await request.json).get('command')
    
    try:
        # Executa o comando no terminal do servidor
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        flash(f"Comando executado com sucesso: {command}", 'success')
        return jsonify({"output": result})
    except subprocess.CalledProcessError as e:
        flash(f"Erro ao executar comando: {e.output}", 'danger')
        return jsonify({"output": e.output})
    from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('terminal.html')

@app.route('/execute', methods=['POST'])
def execute():
    command = request.json.get('command')
    
    try:
        # Executa o comando no terminal do servidor
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return jsonify({"output": result})
    except subprocess.CalledProcessError as e:
        return jsonify({"output": e.output})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
