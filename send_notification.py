# send_notification.py
import asyncio
import websockets
import json

async def send_notification():
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            target_device = input("Ingrese el ID del dispositivo destino: ")
            title = input("Ingrese el título de la notificación: ")
            body = input("Ingrese el cuerpo de la notificación: ")
            
            message = {
                "action": "send_notification",
                "target_device": target_device,
                "message": {
                    "title": title,
                    "body": body
                }
            }
            await websocket.send(json.dumps(message))
            print("Notificación enviada")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_notification())