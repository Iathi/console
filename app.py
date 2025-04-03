from flask import Flask, render_template
import threading
import bot  # Importa o bot.py para rodar junto com Flask

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
            
