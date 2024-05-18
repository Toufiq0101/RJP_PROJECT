from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
import uvicorn
import asyncio
import cv2

app = FastAPI()

async def stream_video(websocket: WebSocket, camera: cv2.VideoCapture):
    await websocket.accept()
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
              
                resized_frame = cv2.resize(frame, (352, 220))
                # resized_frame = cv2.resize(frame, (640, 480))  

                ret, buffer = cv2.imencode('.jpg', resized_frame)
                if not ret:
                    break
                await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(0.05) 
    except (WebSocketDisconnect, ConnectionClosed):
        print("Client disconnected")

@app.websocket("/ws/{id}")
async def get_stream(id: str, websocket: WebSocket):
    camera = cv2.VideoCapture(f'rtmp://122.200.18.78/live/{id}')
    try:
        await stream_video(websocket, camera)
    finally:
        camera.release()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=7885)
