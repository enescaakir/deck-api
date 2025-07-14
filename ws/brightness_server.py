import asyncio
import websockets
import screen_brightness_control as sbc

connected_clients = set()

async def notify_clients(new_brightness):
    if connected_clients:
        await asyncio.gather(*(client.send(str(new_brightness)) for client in connected_clients))

async def watch_brightness(callback, interval=3):
    try:
        last_brightness = sbc.get_brightness(display=0)[0]
    except Exception as e:
        print("[BR] Failed to retrieve the initial brightness level: ", e)
        last_brightness = None

    while True:
        await asyncio.sleep(interval)
        try:
            current_brightness = sbc.get_brightness(display=0)[0]
            if current_brightness != last_brightness:
                last_brightness = current_brightness
                print(f"[BR] Brightness level changed: {current_brightness}%")
                await callback(current_brightness)
        except Exception as e:
            print("[BR] Brightness level action error:", e)

async def websocket_handler(websocket):
    print(f"[BR] [+] New client: {websocket.remote_address}")
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)
        print(f"[BR] [-] Client left: {websocket.remote_address}")

async def start_brightness_ws_server():
    print("🟡 Brightness WebSocket starting: ws://localhost:5050")
    ws_server = await websockets.serve(websocket_handler, "localhost", 5050)
    await asyncio.gather(
        watch_brightness(notify_clients),
        ws_server.wait_closed()
    )
