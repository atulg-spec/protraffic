import requests

def get_geolocation(proxy):
    # Set up the proxy for the request
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    
    # API URL for IP information
    url = 'https://ipinfo.io/json'
    
    try:
        # Make a request to the geolocation API via the proxy
        response = requests.get(url, proxies=proxies, timeout=10)
        data = response.json()

        if 'ip' in data:
            print(f"IP: {data['ip']}")
            print(f"City: {data['city']}")
            print(f"Region: {data['region']}")
            print(f"Country: {data['country']}")
            print(f"Location: {data['loc']}")
            print(f"ISP: {data.get('org', 'N/A')}")
        else:
            print(f"Failed to retrieve geolocation. Response: {data}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting through proxy {proxy}: {e}")

# Example proxy
proxy = "162.19.7.56:32437"
get_geolocation(proxy)
proxy = "162.0.220.217:48824"	
get_geolocation(proxy)
proxy = "162.0.220.161:31963"
get_geolocation(proxy)
