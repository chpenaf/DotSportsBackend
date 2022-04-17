import imp
import requests

def generate_request(url, params={}):
    
    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
        }
    )

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
