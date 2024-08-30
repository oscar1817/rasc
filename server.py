# server.py
import asyncio
import websockets
import json
import firebase_admin
from firebase_admin import credentials, messaging

# Inicializar Firebase Admin SDK
cred = credentials.Certificate("path/to/your/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

connected_clients = {}

async def handle_client(websocket, path):
    device_id = None
    try:
        async for message in websocket:
            data = json.loads(message)
            if data['action'] == 'register':
                device_id = data['device_id']
                fcm_token = data['fcm_token']
                connected_clients[device_id] = {'websocket': websocket, 'fcm_token': fcm_token}
                print(f"Dispositivo registrado: {device_id}")
            elif data['action'] == 'send_notification':
                await send_notification(data['target_device'], data['message'])
    finally:
        if device_id:
            del connected_clients[device_id]

async def send_notification(target_device, message):
    if target_device in connected_clients:
        try:
            await connected_clients[target_device]['websocket'].send(json.dumps(message))
            print(f"Notificación enviada por WebSocket a {target_device}")
        except websockets.exceptions.ConnectionClosed:
            send_fcm_notification(target_device, message)
    else:
        send_fcm_notification(target_device, message)

def send_fcm_notification(target_device, message):
    if target_device in connected_clients and connected_clients[target_device]['fcm_token']:
        fcm_message = messaging.Message(
            data=message,
            token=connected_clients[target_device]['fcm_token'],
        )
        response = messaging.send(fcm_message)
        print(f"Notificación FCM enviada a {target_device}: {response}")
    else:
        print(f"No se pudo enviar notificación a {target_device}: Token FCM no disponible")

async def start_server():
    server = await websockets.serve(handle_client, "localhost", 8765)
    print("Servidor iniciado en ws://localhost:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_server())