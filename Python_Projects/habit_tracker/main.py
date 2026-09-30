import requests
from datetime import datetime

# ---------------------------- CONSTANTS ------------------------------- #

USER_NAME = "hari72"
TOKEN = "zxcvbnmasdf12"
GRAPH_ID = "reading1"

BASE_URL = "https://pixe.la/v1/users"

headers = {
    "X-USER-TOKEN": TOKEN
}

today = datetime.now()
date = today.strftime("%Y%m%d")

# ---------------------------- ADD A PIXEL ------------------------------- #

pixel_endpoint = f"{BASE_URL}/{USER_NAME}/graphs/{GRAPH_ID}"

pixel_data = {
    "date": date,
    "quantity": input("How many hours did you read today? ")
}

response = requests.post(
    url=pixel_endpoint,
    json=pixel_data,
    headers=headers
)

print("POST:", response.text)

# ---------------------------- UPDATE A PIXEL ------------------------------- #

# update_endpoint = f"{BASE_URL}/{USER_NAME}/graphs/{GRAPH_ID}/{date}"
#
# new_pixel_data = {
#     "quantity": "4.5"
# }
#
# response = requests.put(
#     url=update_endpoint,
#     json=new_pixel_data,
#     headers=headers
# )
#
# print("PUT:", response.text)

# ---------------------------- DELETE A PIXEL ------------------------------- #

# delete_endpoint = f"{BASE_URL}/{USER_NAME}/graphs/{GRAPH_ID}/{date}"
#
# response = requests.delete(
#     url=delete_endpoint,
#     headers=headers
# )

print("DELETE:", response.text)

import webbrowser

graph_url = f"https://pixe.la/v1/users/{USER_NAME}/graphs/{GRAPH_ID}.html"
webbrowser.open(graph_url)