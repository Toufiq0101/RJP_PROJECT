import mysql.connector


def fetch_ws_link(auth_id: str, filter_by: str, offset: str, filter_data: [str]):
    # auth_id, filter_by, offset, filter_data = {
    #     "auth_id": auth_id,
    #     "filter_by": filter_by,
    #     "offset": offset,
    #     "filter_data": filter_data,
    # }
    response = []
    con = mysql.connector.connect(
        host="localhost", user="root", password="", database="xyz"
    )
    cursor = con.cursor()
    if filter_by == "area":
        query2 = f"select location,status,area,cam_url,cam_id from camera where auth_id = '{auth_id}' AND area in ({filter_data})"
    # elif data["filter_by"] == ""
    else:
        query2 = f"select location,status,area,cam_url,cam_id from camera where auth_id = '{auth_id}'"
    cursor.execute(query2)
    table = cursor.fetchall()
    for row in table:
        r = {
            "location": f"{row[0]}",
            "status": f"{row[1]}",
            "area": f"{row[2]}",
            "url": f"{row[3]}",
            "id": f"{row[4]}"
        }
        response.append(r)
    cursor.close()
    con.close()
    return response
