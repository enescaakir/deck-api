import asyncio
import websockets
from services import volume

connected_clients = set()

async def notify_clients(new_volume):
    if connected_clients:
        await asyncio.gather(*(client.send(str(new_volume)) for client in connected_clients))

async def watch_volume(callback, interval=0):
    last_volume = None
    while True:
        await asyncio.sleep(interval)
        try:
            current_volume = volume.get_volume()
            if current_volume != last_volume:
                if(last_volume is not None):
                    print(f"Volume changes: {current_volume}%")
                    
                last_volume = current_volume
                await callback(current_volume)
        except Exception as e:
            print("Volume action error:", e)

async def websocket_handler(websocket):
    print(f"[VOL] [+] New client: {websocket.remote_address}")
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)
        print(f"[VOL] [-] Client left: {websocket.remote_address}")

async def start_volume_ws_server():
    print("🟡 Volume WebSocket starting: ws://localhost:5051")
    ws_server = await websockets.serve(websocket_handler, "localhost", 5051)
    await asyncio.gather(
        watch_volume(notify_clients),
        ws_server.wait_closed()
    )
