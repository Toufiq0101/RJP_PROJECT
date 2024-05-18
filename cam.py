# import asyncio
# import websockets

# async def send_message(websocket):
#     while True:
#         await websocket.send("This is a message sent every 5 seconds")
#         await asyncio.sleep(5)  # Wait for 5 seconds

# async def echo(websocket):
#     send_task = asyncio.create_task(send_message(websocket))
#     async for message in websocket:
#         await websocket.send(message)

# async def main():
#     async with websockets.serve(echo, "localhost", 5669):
#         print("WebSocket server started at ws://localhost:5669")
#         await asyncio.Future()  # run forever

# # asyncio.run(main())

# from fastapi import FastAPI, WebSocket
# import uvicorn
# app = FastAPI()

# # WebSocket endpoint to send text data
# @app.websocket("/send_text/{aa}")
# async def send_text(websocket: WebSocket,aa):
#     await websocket.accept()
#     try:
#         # while True:
#         data = await websocket.receive_text()  # Receive text data from the client
#         # Process the received data if needed
#         if data:
#             print("Received:")
#             await websocket.send_text(f"Echo: kkkk")
#         print("testing from fastapi")
#     except Exception as e:
#         print("WebSocket connection closed:", e)

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=5669)




from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

connected_websockets: List[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  connected_websockets.append(websocket)
  try:
    while True:
      data = await websocket.receive_text()
      # Forward the message to all connected clients
      for ws in connected_websockets:
        if ws != websocket:  # Avoid sending back to the sender
          await ws.send_text(data)
    print(connected_websockets)
  except WebSocketDisconnect:
    if websocket in connected_websockets:
        connected_websockets.remove(websocket)
  finally:
    if websocket in connected_websockets:
        connected_websockets.remove(websocket)

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=5669)
