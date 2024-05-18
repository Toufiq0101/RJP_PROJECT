from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import mysql.connector
import multiprocessing
import tensorflow as tf
import os
from fastapi import (
    FastAPI,
    Request,
    WebSocket,
    WebSocketDisconnect,
    UploadFile,
    File,
    Form,
)
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import os
from face_searching.fr import live_face_srching_api as f_srch
from fastapi.responses import FileResponse
from typing import List


app = FastAPI()
origins = ["http://localhost", "http://localhost:5173", "*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def test():
    return "test"


# SEARCH LICENSE PLATE
class introgate_vehicle_data(BaseModel):
    srch_license_plate: str
    auth_id: str
    dvr_id: str


@app.get("/interogate/license_plate")
async def root(kkk, item: introgate_vehicle_data, q: str | None = None):

    from num_plate_searching.new import process_video

    r = {"a": kkk, **item.dict()}

    yolo_coco_model_path = "/home/devendra/apis/num_plate_searching/yolov8n.pt"
    yolo_license_plate_model_path = (
        "/home/devendra/apis/num_plate_searching/license_plate_detector.pt"
    )
    video_path = [
        "/home/devendra/apis/num_plate_searching/car1.mp4",
        "/home/devendra/apis/num_plate_searching/car3.mp4",
    ]
    srch_number_plate = r["srch_license_plate"]
    found, camera_id = process_video(
        yolo_coco_model_path,
        yolo_license_plate_model_path,
        video_path[1],
        srch_number_plate,
    )
    print(found, camera_id)
    if found:
        res = {
            "loc": [
                ("26.910610283265367", "75.81843318045959"),
                ("26.910656629773012", "75.8184539703225"),
            ],
            "time_stamp": "1714147430",
            "auth_id": found,
            "cam_id": camera_id,
        }
    else:
        res = "Suspect Not Found"

    return res


# SHOW DVR
class DVR_req(BaseModel):
    auth_id: str
    areas: str


@app.post("/show/dvr")
async def show_dvr(item: DVR_req):
    from db.dvr import show_dvr

    data = {**item.dict()}
    print(data)
    response = show_dvr(data["auth_id"], data["areas"])
    return response


# ADD DVR
class DVR_data(BaseModel):
    auth_id: str
    dvr_name: str
    dvr_status: str
    dvr_location: str
    associated_cam: str
    ownership: str
    owner_name: str
    storage: str
    mac: str


@app.get("/register")
async def register_dvr(item: DVR_data):
    """
        {
        "auth_id":"str",
        "dvr_name":"str",
        "dvr_status":"str"
        "dvr_location":"str",
        "associated_cam":"str",
        "ownership":"ollol",
        "owner_name":"str",
        "storage":"str",
        "mac":"str"
    }
    """
    from db.dvr import add_dvr

    data = {**item.dict()}
    print(data)
    reponse = add_dvr()
    return data


# Fetch Camera's rtmp link
@app.get("/cam/url")
async def get_cam_url():
    from db.cam import fetch_ws_link

    data = fetch_ws_link(auth_id="999", filter_by="*", offset="10-20", filter_data="")
    # urls = []
    # for row in data:
    #     print(row)
    #     location, status, area, url, id = row
    #     urls.append(url)
    return data


class map_data(BaseModel):
    auth_id: str
    # areas:str


@app.post("/map/all")
async def get_all_locs(data: map_data):
    from db.map import get_dvr_coords

    auth_id = {**data.dict()}["auth_id"]
    return get_dvr_coords(auth_id)


# SEARCH PERSON'S FACE IN LIVE FEED

# Get the current directory where the script is located
# current_directory = os.path.dirname(os.path.abspath(__file__))
# @app.post("/search/person/")
# async def upload_images(
#     files: list[UploadFile] = File(...), textInputs: list = Form(...)
# ):
#     # responses = []
#     print(textInputs)
#     print(files)
#     img_files = []
#     for file in files:
#         # Save the uploaded file in the current directory
#         file_path = os.path.join(current_directory, "./input/", file.filename)
#         with open(file_path, "wb") as buffer:
#             buffer.write(await file.read())
#         img_files.append(f"D:/Rajasthan_Project/apis/input/{file.filename}")
#     # print(textInputs)
#     auth_id = ""
#     filter_by = ""
#     filter_data = ""
#     for textInput in textInputs:
#         print("Received text:", textInput)
#     # print(img_files)

#     # CALL API
#     response = f_srch.initiate_face_srch("ABC123", "area", "814110", img_files)
#     for i,r in enumerate(response):
#         response[i]["img"] = FileResponse(r["img_name"])
#     return response
current_directory = os.path.dirname(os.path.abspath(__file__))

@app.post("/search/person/")
async def upload_images(files: list[UploadFile] = File(...)):
    # responses = []
    print(files)
    img_files = []
    for file in files:
        # Save the uploaded file in the current directory
        file_path = os.path.join(current_directory, "./input/", file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        img_files.append(f"D:/Rajasthan_Project/apis/input/{file.filename}")
    # print(textInputs)
    auth_id = ""
    filter_by = ""
    filter_data = ""
    # print(img_files)

    # CALL API
    # img_files = [
    #     # "D:/Rajasthan_Project/apis/face_searching/fr/known_people/Sagar_Shukla.jpg",
    #     # "D:/Rajasthan_Project/apis/face_searching/fr/known_people/Chandresh.jpg",
    #     # "D:/Rajasthan_Project/apis/face_searching/fr/known_people/Marcus_Michael.jpg",
    #     "D:/Rajasthan_Project/apis/face_searching/fr/known_people/Toufiq.png",
    # ]
    response = f_srch.initiate_face_srch("ABC123", "area", "814110", img_files)
    for i, r in enumerate(response):
        response[i]["img"] = FileResponse(r["img_name"])
    return response


connected_websockets: List[WebSocket] = []
# face-search result websocket endpoint
@app.websocket("/fsr_ws")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  connected_websockets.append(websocket)
  try:
    while True:
      data = await websocket.receive_text()
      for ws in connected_websockets:
        if ws != websocket:
          await ws.send_text(data)
    print(connected_websockets)
  except WebSocketDisconnect:
    if websocket in connected_websockets:
        connected_websockets.remove(websocket)
  finally:
    if websocket in connected_websockets:
        connected_websockets.remove(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5667)
