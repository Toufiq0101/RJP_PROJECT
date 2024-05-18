import asyncio
import multiprocessing
import websocket
import time
def timer():
    time.sleep(2)
    return 1
async def async_func():
    ws = websocket.create_connection("ws://127.0.0.1:5669/ws")
    print("Async function started")
    print("Async function finished")
    if timer():
        ws.send(f"hhhhhhhhhhhhhhhh")
    # if await asyncio.sleep(1):
    #     print("connection_closing")
    #     await asyncio.Future()
    #     print("T")
    #     await future
    #     print("r")
    #     future.cancel()
    #     print("L")

def run_async_func():
    print("pppp")
    asyncio.run(async_func())
    print("test1")

if __name__ == "__main__":
    # ws = websocket.create_connection("ws://127.0.0.1:5669/send_text")
    print("test")
    # Create a multiprocessing process
    p = multiprocessing.Process(target=run_async_func)

    # Start the process
    p.start()

    # Wait for the process to finish
    p.join()
