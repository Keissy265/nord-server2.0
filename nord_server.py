from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def home():
    return "✅ Nord Server 2.0 is running!"

@socketio.on("connect")
def handle_connect():
    print("🔌 Client connected!")
    emit("server_message", {"data": "Welcome to Nord Server 2.0!"})

@socketio.on("message")
def handle_message(data):
    print(f"📩 Message received: {data}")
    emit("server_message", {"data": f"Echo: {data}"}, broadcast=True)

@socketio.on("disconnect")
def handle_disconnect():
    print("❌ Client disconnected!")

# ===========================
# 🔁 BOT RELAY ENDPOINTS BELOW
# ===========================

# Receive updates from the bot and send to frontend
@app.route("/bot_update", methods=["POST"])
def bot_update():
    data = request.json
    print(f"🤖 Bot update: {data}")
    socketio.emit("bot_update", data, broadcast=True)
    return {"status": "ok"}, 200

# Simple test endpoint to verify connection
@app.route("/ping")
def ping():
    return {"status": "online", "server": "Nord 2.0"}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Running Nord server on port {port}")
    socketio.run(app, host="0.0.0.0", port=port, allow_unsafe_werkzeug=True)
