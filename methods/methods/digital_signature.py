
API_URL = "https://api.docuseal.com"
API_KEY = "dV6jEmhUsmbV2ipawZPmD784YPEYyHNuBEh96yMjn8y"
import requests

headers = {
    "X-Auth-Token": API_KEY,
    "Content-Type": "application/json"
}

data = {
    "template_id": 123,
    "order": "preserved",
    "submitters": [
        {
            "email": "john.doe@example.com",
            "role": "Director"
        },
        {
            "email": "roe.moe@example.com",
            "role": "Contractor"
        }
    ]
}

response = requests.post(API_URL, headers=headers, json=data)

if response.status_code == 200:
    # Assuming response data is a list and we want the 'slug' of the first item
    print(response.json()[0]["slug"])
else:
    print(f"Error: {response.status_code} - {response.text}")
