import requests

# URL for the IP lookup
url = 'https://ipwhois.app/json/'

# Proxy details
proxy = {
    "http": "http://fazli31-zone-resi-region-us-session-c168983aabda-sessTime-120:rabi786@4e52f83007cd8a41.ika.na.pyproxy.io:16666",
    "https": "http://fazli31-zone-resi-region-us-session-c168983aabda-sessTime-120:rabi786@4e52f83007cd8a41.ika.na.pyproxy.io:16666"
}

try:
    # Making the request using the proxy
    response = requests.get(url, proxies=proxy, timeout=10)

    # Checking if the request was successful
    if response.status_code == 200:
        print("Response JSON:", response.json())
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

except requests.exceptions.ProxyError as e:
    print(f"Proxy error: {e}")
except requests.exceptions.Timeout:
    print("The request timed out")
except Exception as e:
    print(f"An error occurred: {e}")
