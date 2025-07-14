import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from api.routes import router
from ws.volume_server import start_volume_ws_server
from ws.brightness_server import start_brightness_ws_server
from ws.wallpaper_server import start_wallpaper_ws_server

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(start_volume_ws_server())
    asyncio.create_task(start_brightness_ws_server())
    asyncio.create_task(start_wallpaper_ws_server())
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=2837, reload=True)