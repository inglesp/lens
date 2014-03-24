import requests

BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json'

class LatLngError(Exception):
    pass


def get_latlng(address_elements):
    params = {
        'address': ', '.join(element for element in address_elements if element),
        'sensor': 'false',
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data['status'] == 'OK':
        if len(data['results']) > 1:
            raise LatLngError('Multiple results returned')
        else:
            result = data['results'][0]
            location = result['geometry']['location']
            return location['lat'], location['lng']
    elif data['status'] == 'ZERO_RESULTS':
        raise LatLngError('No results returned')
    else:
        message = '{} ({})'.format(data['status'], data.get('error_message', 'no specific error'))
        raise LatLngError(message)
