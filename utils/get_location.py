import asyncio

import requests


async def get_full_address(longitude, latitude):
    """This is open source map api to get full address, if it does not work return False"""
    await asyncio.sleep(1)
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
    headers = {
        "User-Agent": "n50_evos/1.0 (baxromovna6974@gmail.com)"
    }
    response = requests.get(url=url, headers=headers)

    if response.status_code == 200:
        return response.json()['display_name']
    return False
