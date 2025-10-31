import asyncio
import websockets
import json
import os

DERIV_APP_ID = "109202"
DERIV_TOKEN = "JI3uwFsEkJUkViz"

clients = set()

async def deriv_stream():
    url = f"wss://ws.derivws.com/websockets/v3?app_id={DERIV_APP_ID}"
    async with websockets.connect(url) as ws:
        await ws.send(json.dumps({"authorize": DERIV_TOKEN}))
        await ws.recv()
        await ws.send(json.dumps({"ticks_subscribe": "R_100"}))
        print("✅ Subscribed to ticks...")

        while True:
            msg = await ws.recv()
            for client in clients:
                try:
                    await client.send(msg)
                except:
                    pass

async def client_handler(websocket, path):
    clients.add(websocket)
    try:
        async for msg in websocket:
            print("📩 Client message:", msg)
    finally:
        clients.remove(websocket)

async def main():
    server = await websockets.serve(client_handler, "0.0.0.0", int(os.environ.get("PORT", 8080)))
    print("🚀 Nord Server running on Render...")
    await deriv_stream()
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
