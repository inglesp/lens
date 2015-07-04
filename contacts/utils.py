from time import sleep

import requests

from .exceptions import LatLngError, OverQueryLimitError

BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json'


def get_latlng(address_elements, attempt=0):
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
    elif data['status'] == 'OVER_QUERY_LIMIT':
        if attempt < 5:
            print "We have temporarily exceeded Google's query limit -- sleeping for 30s"
            sleep(30)
            return get_latlng(address_elements, attempt + 1)
        else:
            raise OverQueryLimitError
    else:
        message = '{} ({})'.format(data['status'], data.get('error_message', 'no specific error'))
        raise LatLngError(message)
