import requests

# Proxy string (assuming it's in the format provided earlier)
proxy = "93005287DkEr-zone-custom-region-us-sessid-nwu2m71k-sessTime-120:be48194135@107.150.106.39:3660"

# Extract credentials and IP:port from the proxy string
credentials, ip_port = proxy.split('@')
username, password = credentials.split(':')[0], credentials.split(':')[1]

# Setup the proxy dictionary with authentication for requests
proxies = {
    "http": f"http://{username}:{password}@{ip_port}",
    "https": f"https://{username}:{password}@{ip_port}",
}
# Using an IP geolocation API like ipinfo.io or ip-api.com
url = "http://ip-api.com/json"

try:
    # Make a request through the proxy
    response = requests.get(url, proxies=proxies, timeout=10)
    data = response.json()

    # Extract relevant information
    ip_address = data.get("query", "N/A")
    country = data.get("country", "N/A")
    region = data.get("regionName", "N/A")
    city = data.get("city", "N/A")
    timezone = data.get("timezone", "N/A")

    # Print the results
    print(f"IP Address: {ip_address}")
    print(f"Country: {country}")
    print(f"Region: {region}")
    print(f"City: {city}")
    print(f"Timezone: {timezone}")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
