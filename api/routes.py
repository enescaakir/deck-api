import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from services import brightness, system, notifier, volume

router = APIRouter()
volume_precise = 1000
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Audio Control
@router.get("/volume")
async def volume_route(level: str = None):
    if level is None:
        return volume.get_volume()
    elif level.isdigit():
        volume.set_volume(int(level))
    elif level == "up":
        volume.change_volume(volume_precise)
    elif level == "down":
        volume.change_volume(-volume_precise)
    elif level == "mute":
        volume.toggle_mute()
    else:
        raise HTTPException(status_code=400, detail="Invalid parameters. Use 'up' / 'down' / 'mute' or no parameter.")

    current_level = volume.get_volume()
    await notifier.broadcast(str(current_level))
    return {"success": True}

# Brightness Control
@router.get("/brightness")
async def set_brightness(level: str = None):
    try:
        if level is None:
            return brightness.get_brightness()
        if not level.isdigit():
            raise HTTPException(status_code=400, detail="Brightness must be between 0 and 100")
        brightness.set_brightness(int(level))

        current_level = brightness.get_brightness()
        await notifier.broadcast(str(current_level))

        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# System Control
@router.get("/system")
async def system_control(action: str):
    if action == "shutdown":
        system.shutdown()
    elif action == "standby":
        system.standby()
    elif action == "lock":
        system.lock_screen()
    else:
        raise HTTPException(status_code=400, detail="Invalid parameter. Use 'shutdown' / 'standby' / 'lock'.")
    return {"success": True}

# Background
@router.get("/bg")
def get_wallpaper():
    file_path = os.path.join("static", "wallpaper.jpg")
    return FileResponse(file_path, media_type="image/jpeg")