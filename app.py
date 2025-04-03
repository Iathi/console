from flask import Flask, render_template
import threading
import bot  # Importa o bot.py para rodar junto com Flask

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    threading.Thread(target=bot.run_bot).start()  # Inicia o bot em paralelo
    app.run(debug=True, host="0.0.0.0", port=5000)
