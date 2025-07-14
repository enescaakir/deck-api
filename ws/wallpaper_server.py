import asyncio
import websockets
from os import path, getcwd
import services.wallpaper as wallpaperService

connected_clients = set()

async def notify_clients(new_wallpaper_path):
    if connected_clients:
        await asyncio.gather(*(client.send(new_wallpaper_path) for client in connected_clients))

async def watch_wallpaper(callback, interval=1):
    try:
        last_path = wallpaperService.get_wallpaper_path()
    except Exception as e:
        print("[WP] Failed to retrieve the initial wallpaper path.", e)
        last_path = None

    while True:
        await asyncio.sleep(interval)
        try:
            current_path = wallpaperService.get_wallpaper_path()
            if current_path != last_path:
                last_path = current_path
                wallpaperService.copy_wallpaper()
                copied_wallpaper_path = path.join(getcwd(), 'static', "wallpaper.jpg")
                print(f"[WP] Wallpaper changed: {copied_wallpaper_path}")
                await callback(copied_wallpaper_path)
        except Exception as e:
            print("[WP] Wallpaper action error:", e)

async def websocket_handler(websocket):
    print(f"[WP] [+] New client: {websocket.remote_address}")
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)
        print(f"[WP] [-] Client left: {websocket.remote_address}")

async def start_wallpaper_ws_server():
    print("🟡 Wallpaper WebSocket starting: ws://localhost:5052")
    ws_server = await websockets.serve(websocket_handler, "localhost", 5052)
    await asyncio.gather(
        watch_wallpaper(notify_clients),
        ws_server.wait_closed()
    )