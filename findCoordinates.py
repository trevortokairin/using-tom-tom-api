import requests
import pandas as pd
import math
import time

def findCoordinates(address, key=None):
    # personal API key
    personal_key = 'RWA40PGejppxkMcWo9QAcmtBGdplEA2I'

    if key is None:
        key = personal_key

    # Initialize the DataFrame
    df = pd.DataFrame(columns=['lat', 'lng', 'address', 'status_code'])

    for addr in address:
        # Replace special characters with their hexadecimal equivalents
        query = addr.replace(" ", "%20").replace(",", "%2C").replace("#", "%23")

        # Construct the API query
        url = f"https://api.tomtom.com/search/2/geocode/{query}.json?key={key}"

        # Execute the query
        response = requests.get(url)

        # Check if the query is successful
        if response.status_code == 200:
            try:
                data = response.json()
                if data['results']:
                    # Check if there are multiple sets of coordinates
                    if 'entryPoints' in data['results'][0]:
                        # Find the first entry point with a type of 'main'
                        for entryPoint in data['results'][0]['entryPoints']:
                            if entryPoint['type'] == 'main':
                                lat = entryPoint['position']['lat']
                                lng = entryPoint['position']['lon']
                                break
                    else:
                        lat = data['results'][0]['position']['lat']
                        lng = data['results'][0]['position']['lon']
                    addr = data['results'][0]['address']['freeformAddress']
                else:
                    lat = math.nan
                    lng = math.nan
            except ValueError:
                lat = math.nan
                lng = math.nan
        elif response.status_code == 403 and addr == '???':
            # Handle invalid addresses
            lat = math.nan
            lng = math.nan
            response.status_code = 404
        else:
            lat = math.nan
            lng = math.nan

        # Append the result to the DataFrame
        df = pd.concat([df, pd.DataFrame({'lat': [lat], 'lng': [lng], 'address': [addr], 'status_code': [response.status_code]})], ignore_index=True)

        # Sleep for 1 second to limit the rate of API requests
        time.sleep(1)

    return df













