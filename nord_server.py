from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import random
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store latest ticks
latest_ticks = []

@app.route('/')
def home():
    return jsonify({"status": "Nord AI Python Server is running..."})

@app.route('/tick', methods=['POST'])
def receive_tick():
    data = request.get_json()
    if not data or "tick" not in data:
        return jsonify({"error": "Invalid data"}), 400

    latest_ticks.append(data["tick"])
    if len(latest_ticks) > 50:
        latest_ticks.pop(0)

    # Emit tick to all websocket clients
    socketio.emit("tick_update", {"tick": data["tick"]})
    return jsonify({"status": "received"})


# Simple random decision for demo
@socketio.on("request_decision")
def handle_decision(data):
    # Random signal for now
    decision = random.choice(["BUY", "SELL", "HOLD"])
    print(f"Decision sent: {decision}")
    emit("trade_signal", {"signal": decision})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
