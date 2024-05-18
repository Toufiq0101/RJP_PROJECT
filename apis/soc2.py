from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
import uvicorn
import asyncio
import cv2

# Install Fastapi, websockets, Jinja2
app = FastAPI()
# camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)

@app.websocket("/ws/{id}")
async def get_stream(id, websocket: WebSocket):
    camera = cv2.VideoCapture(f"rtmp://122.200.18.78/live/web")
    await websocket.accept()
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode(".jpg", frame)
                await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(0.001)
    except (WebSocketDisconnect, ConnectionClosed):
        print("Client disconnected")


@app.get("/")
async def test():
    return "tested"


if __name__ == "__main__":
    # uvicorn.run(app, host='127.0.0.1', port=8000)
    uvicorn.run(app, host="0.0.0.0", port=7880)
