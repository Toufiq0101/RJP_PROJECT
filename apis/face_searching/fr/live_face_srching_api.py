import mysql.connector
from .srch_in_multiple_stream import api_call

# import srch_in_multiple_stream as smst

def initiate_face_srch(auth_id: str, filter_by: str, filter_data: [str], img_list):
    camera_url_list = []
    face_img_list = []
    cam_id_list = []
    response = []
    db_data = []
    con = mysql.connector.connect(
        host="localhost", user="root", password="", database="xyz"
    )
    cursor = con.cursor()
    if filter_by == "area":
        query2 = f"select location,status,area,rtsp_cam_url,cam_id from camera where auth_id = '{auth_id}' AND area in ({filter_data})"
    else:
        query2 = f"select location,status,area,rtsp_cam_url,cam_id from camera where auth_id = '{auth_id}'"
    cursor.execute(query2)
    table = cursor.fetchall()
    for row in table:
        camera_url_list.append(row[3])
        cam_id_list.append(row[4])
        r = {
            "location": f"{row[0]}",
            "status": f"{row[1]}",
            "area": f"{row[2]}",
            "url": f"{row[3]}",
            "id": f"{row[4]}",
        }
        db_data.append(r)
    cursor.close()
    con.close()

    # srch_response_data = {'cam2': {'found': True, 'img_name': 'D:/Rajasthan_Project/apis/output/914.jpg'}, 'cam3': {'found': True, 'img_name': 'D:/Rajasthan_Project/apis/output/209.jpg'}, 'cam1': {'found': True, 'img_name': 'D:/Rajasthan_Project/apis/output/691.jpg'}}
    srch_response_data = api_call(
        cam_list=camera_url_list, img_list=img_list, cam_id=cam_id_list
    )
    # print(srch_response_data)
    for r in db_data:
        if r["id"] in srch_response_data.keys():
            ab = {
                "cam_id" : r["id"],
                "loc" : r["location"],
                "area" : r["area"],
                "img_name" : srch_response_data[r["id"]]["img_name"]
            }
            response.append(ab)
            # return
    # print(response)
    return response

face_img_list = [
    # "D:/Rajasthan_Project/apis/face_searching/fr/known_people/Sagar_Shukla.jpg",
    # "D:/Rajasthan_Project/apis/face_searching/fr/known_people/Chandresh.jpg",
    # "D:/Rajasthan_Project/apis/face_searching/fr/known_people/Marcus_Michael.jpg",
    "D:/Rajasthan_Project/apis/face_searching/fr/known_people/Toufiq.png",
]
if __name__ == "__main__":
    print(initiate_face_srch("ABC123", "area", "814110", face_img_list))
