import random

def generate_user_agents():
    windows_versions = ["Windows NT 7.0", "Windows NT 8.0", "Windows NT 10.0", "Windows NT 11.0"]
    mobile_devices = [
        "iPhone; CPU iPhone OS 15_0 like Mac OS X", 
        "iPhone; CPU iPhone OS 14_0 like Mac OS X", 
        "Android 11; Mobile; rv:89.0", 
        "Android 10; Mobile; rv:87.0", 
        "Android 9; Mobile; Chrome/86.0.4240.198"
    ]
    browsers = [
        "Mozilla/5.0", 
        "Mozilla/4.0"
    ]
    platforms = ["Win64; x64", "WOW64", "x86_64", "iPhone", "Linux; Android 11", "Linux; Android 10"]
    engines = [
        "AppleWebKit/537.36 (KHTML, like Gecko)", 
        "Gecko/20100101 Firefox/89.0", 
        "Chrome/92.0.4515.159 Safari/537.36", 
        "Edg/92.0.902.84", 
        "Chrome/91.0.4472.124 Mobile Safari/537.36"
    ]
    
    user_agents = []
    
    for _ in range(500):
        if random.choice([True, False]):  # Windows devices
            os_version = random.choice(windows_versions)
            platform = random.choice(platforms[:3])  # Select platform for desktop
        else:  # Mobile devices
            os_version = random.choice(mobile_devices)
            platform = random.choice(platforms[3:])  # Select platform for mobile

        browser = random.choice(browsers)
        engine = random.choice(engines)

        user_agent = f"{browser} ({os_version}; {platform}) {engine}"
        user_agents.append(user_agent)
    
    return user_agents

# Generate and print user agents
user_agents = generate_user_agents()
for ua in user_agents:
    print(ua)
