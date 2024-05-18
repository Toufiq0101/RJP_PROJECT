, WebSocket
# import uvicorn
# app = FastAPI()

# # WebSocket endpoint to send text data
# @app.websocket("/send_text/{aa}")
# async def send_text(websocket: WebSocket,aa):
#     # await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()  # Receive text data from the client
#             # Process the received data if needed
#             print("Received:", data)
#             await websocket.send_text(f"Echo: kkkk")
#         print("testing from fastapi")
#     except Exception as e:
#         print("WebSocket connection closed:", e)

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=5669)
