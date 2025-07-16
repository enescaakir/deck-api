# 🎮 Deck API

**Deck API** is a powerful system control API developed for Windows systems. It provides volume, brightness, system power management, and wallpaper control using FastAPI and WebSocket technologies.

## 🌟 Features

- **🔊 Volume Control**: Set volume level, increase/decrease, mute/unmute
- **💡 Brightness Control**: Monitor brightness adjustment, multi-monitor support
- **⚡ System Management**: Shutdown, standby mode, screen lock
- **🖼️ Wallpaper Service**: Access current wallpaper via API
- **🔄 Real-time Monitoring**: Instant change notifications via WebSocket
- **🖥️ Multi-Monitor Support**: Customized brightness settings for different monitors

## 🏗️ Technology Stack

- **Backend**: FastAPI
- **WebSocket**: websockets
- **Volume Control**: pycaw (Windows Audio Session API)
- **Brightness Control**: screen-brightness-control
- **System Control**: Windows API (nircmd, rundll32)
- **Wallpaper**: Windows SystemParametersInfo API

## 📋 Requirements

- **Operating System**: Windows 10/11
- **Python**: 3.9+
- **Additional Tools**: nircmd.exe (for system controls)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/enescaakir/deck-api.git
cd deck-api
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn websockets screen-brightness-control pycaw comtypes python-multipart
```

### 4. Install nircmd.exe
1. Download [NirCmd](https://www.nirsoft.net/utils/nircmd.html) tool
2. Add `nircmd.exe` to system PATH or copy to `C:\Windows\System32` folder

### 5. Start the Application
```bash
python main.py
```

## 🌐 API Endpoints

The API runs on `http://localhost:2837`.

### 🔊 Volume Control
```http
GET /volume              # Get current volume level
GET /volume?level=50     # Set volume to 50
GET /volume?level=up     # Increase volume
GET /volume?level=down   # Decrease volume
GET /volume?level=mute   # Toggle mute
```

### 💡 Brightness Control
```http
GET /brightness          # Get current brightness
GET /brightness?level=75 # Set brightness to 75%
```

### ⚡ System Controls
```http
GET /system?action=shutdown  # Shutdown system
GET /system?action=standby   # Enter standby mode
GET /system?action=lock      # Lock screen
```

### 🖼️ Wallpaper
```http
GET /bg                  # Get current wallpaper
```

## 📡 WebSocket Connections

WebSocket connections for real-time changes:

- **Brightness**: `ws://localhost:5050`
- **Volume**: `ws://localhost:5051`
- **Wallpaper**: `ws://localhost:5052`

### WebSocket Example
```javascript
const volumeSocket = new WebSocket('ws://localhost:5051');
volumeSocket.onmessage = (event) => {
    console.log('Volume level:', event.data);
};
```

## 📁 Project Structure

```
deck-api/
├── main.py                 # Main application file
├── api/
│   └── routes.py          # API endpoints
├── services/
│   ├── brightness.py      # Brightness control
│   ├── notifier.py        # Notification service
│   ├── system.py          # System controls
│   ├── volume.py          # Volume control
│   └── wallpaper.py       # Wallpaper operations
├── ws/
│   ├── brightness_server.py  # Brightness WebSocket server
│   ├── volume_server.py      # Volume WebSocket server
│   └── wallpaper_server.py   # Wallpaper WebSocket server
├── static/                   # Static files (wallpaper)
```

## ⚙️ Configuration

### Multi-Monitor Settings
You can edit monitor-specific settings in `services/brightness.py`:

```python
# To see monitor list
def get_monitors():
    return sbc.list_monitors()

# Custom monitor setting
if monitor == 'Philips 246V5':
    value += second_monitor_brightness_additional_value
```

### Volume Sensitivity
You can adjust volume change sensitivity in `api/routes.py`:

```python
volume_precise = 1000  # Volume change amount
```

## 📄 License

This project is licensed under the MIT License.

## 📞 Contact

**Developer**: Enes Çakır  
[**Website**](https://enescakr.com/) | [**GitHub**](https://github.com/enescaakir) | [**Linkedin**](https://www.linkedin.com/in/enescaakir/)

---

⭐ Don't forget to star this project if you like it!
