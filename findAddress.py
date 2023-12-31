import requests
import pandas as pd
import math
import time
from collections.abc import Iterable

def findAddress(lat, lng, key=None):
    # Your personal API key
    personal_key = 'RWA40PGejppxkMcWo9QAcmtBGdplEA2I'

    # Use personal API key if no key is provided
    if key is None:
        key = personal_key

    # Check if lat and lng are iterable
    if not isinstance(lat, Iterable) or not isinstance(lng, Iterable):
        return None

    # Check if lat and lng have the same lengths
    if len(lat) != len(lng):
        return None

    # Initialize lists to store results
    address_list = []
    status_code_list = []

    # Iterate over each set of coordinates
    for lat_val, lng_val in zip(lat, lng):
        # Construct the API query
        url = f'https://api.tomtom.com/search/2/reverseGeocode/{lat_val},{lng_val}.json?key={key}'

        # Execute the query
        response = requests.get(url)

        # Check for rate limit error
        while response.status_code == 429:
            # If rate limit error, wait for 1 second and try again
            time.sleep(1)
            response = requests.get(url)

        data = response.json()

        # Check if query is successful
        if response.status_code == 200 and data['addresses']:
            # Get the first result
            result = data['addresses'][0]

            # Get the address
            address = result['address']['freeformAddress']
        else:
            # If query is not successful, set address to None
            address = None

        # Append results to lists
        address_list.append(address)
        status_code_list.append(response.status_code)

    # Create a DataFrame with the results
    df = pd.DataFrame({
        'address': address_list,
        'status_code': status_code_list
    })

    return df

