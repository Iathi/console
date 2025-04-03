from flask import Flask, jsonify
import os

app = Flask(__name__)

# Simulação de membros online
members_online = ["Carlos", "Ana", "Lucas"]

@app.route('/api/members')
def get_members():
    return jsonify({"members": members_online})

@app.route('/api/logs')
def get_logs():
    if os.path.exists("logs.txt"):
        with open("logs.txt", "r", encoding="utf-8") as file:
            logs = file.read()
    else:
        logs = "Nenhum log disponível"
    return jsonify(logs)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
