import requests
import json
import os

token = os.getenv('AUTHORIZATION_TOKEN')
url = "http://homeassistant.local:8123/api/services/light/turn_on"
headers = {
    "Authorization": "Bearer " + token,
    "content-type": "application/json",
}

def set_color(color_rgb, brightness):
    data = {
        "entity_id": "light.bedroom",
        "rgb_color": color_rgb,
        "brightness": brightness,
        "transition": 1
        }

    response = requests.request('post', url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print(response.text)
