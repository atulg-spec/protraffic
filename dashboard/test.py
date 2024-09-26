import random
import csv

def random_hex_string(length):
    """Generates a random hexadecimal string of a specified length."""
    return ''.join(random.choices('0123456789abcdef', k=length))

def get_user_agents():
    """Returns a list of realistic user agent strings."""
    return [
        # Windows User Agents
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    ]

def generate_fingerprint(user_agents):
    """Generates a single hardware fingerprint dictionary."""
    visitor_id = random_hex_string(40)
    canvas_hash = random_hex_string(40)
    webgl_hash = random_hex_string(40)
    webgl_report = random_hex_string(40)
    
    # Extended list of Unmasked Vendors
    unmasked_vendor = random.choice([
        "Google Inc. (Intel)", 
        "NVIDIA Corporation", 
        "AMD", 
        "Apple Inc.", 
        "Microsoft Corporation", 
        "Intel Corporation", 
        "Qualcomm", 
        "ARM Limited", 
        "Broadcom", 
        "MediaTek",
        "Samsung Electronics",
        "Sony Corporation",
        "ASUS",
        "Dell Inc.",
        "HP Inc.",
        "Lenovo",
        "Huawei Technologies",
        "LG Electronics",
        "Toshiba",
        "Fujitsu",
        "Panasonic Corporation",
        "Acer Inc.",
        "Cisco Systems",
        "Xiaomi",
        "ZTE Corporation",
        "Hewlett Packard Enterprise",
        "OnePlus",
        "Oppo",
        "Vivo",
        "Motorola Mobility",
        "Philips",
        "Sharp Corporation",
        "Hitachi",
        "Kyocera",
        "Mitsubishi Electric",
        "Siemens AG",
        "Foxconn",
        "TCL Corporation",
        "Nokia Corporation",
        "Ericsson",
        "Alcatel-Lucent",
        "Micron Technology",
        "Seagate Technology",
        "Western Digital",
        "Sandisk",
        "Kingston Technology",
        "Logitech",
        "Razer Inc.",
        "Corsair Components",
        "Thermaltake Technology",
        "Gigabyte Technology",
        "MSI (Micro-Star International)"
    ])


    unmasked_renderer = random.choice([
        "ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (Intel, Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (Intel, Intel(R) Iris(R) Plus Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (Intel, Intel(R) Iris(R) Xe Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (NVIDIA, NVIDIA GeForce GTX Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (NVIDIA, NVIDIA GeForce GTX 1080 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (NVIDIA, NVIDIA Quadro P2000 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (NVIDIA, NVIDIA Tesla V100 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (AMD, AMD Radeon RX 580 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (AMD, AMD Radeon RX 5700 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (AMD, AMD Radeon Vega 8 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (AMD, AMD Radeon Pro 5600M Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (AMD, AMD Radeon RX 6900 XT Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (AMD, AMD Radeon RX 550 Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "ANGLE (Apple, Apple M1 GPU Metal vs_5_0 ps_5_0)",
        "ANGLE (Apple, Apple A12Z GPU Metal vs_5_0 ps_5_0)",
        "ANGLE (Apple, Apple A14 Bionic GPU Metal vs_5_0 ps_5_0)",
        "ANGLE (Apple, Apple A15 Bionic GPU Metal vs_5_0 ps_5_0)",
        "ANGLE (Qualcomm, Adreno 620 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Qualcomm, Adreno 630 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Qualcomm, Adreno 650 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Qualcomm, Adreno 660 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Qualcomm, Adreno 530 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (ARM, Mali-G76 OpenGL ES 3.2 vs_5_0 ps_5_0)",
        "ANGLE (ARM, Mali-G77 OpenGL ES 3.2 vs_5_0 ps_5_0)",
        "ANGLE (ARM, Mali-G78 OpenGL ES 3.2 vs_5_0 ps_5_0)",
        "ANGLE (ARM, Mali-T880 OpenGL ES 3.2 vs_5_0 ps_5_0)",
        "ANGLE (ARM, Mali-G52 OpenGL ES 3.2 vs_5_0 ps_5_0)",
        "ANGLE (Samsung, Exynos 2100 GPU Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Samsung, Exynos 9810 GPU Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Samsung, Exynos 990 GPU Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Samsung, Exynos 8895 GPU Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Sony, PlayStation 5 GPU Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Sony, PlayStation 4 Pro GPU Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Sony, PlayStation 4 GPU Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Microsoft, Xbox Series X GPU Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Microsoft, Xbox Series S GPU Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Microsoft, Xbox One X GPU Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Microsoft, Surface Pro X GPU Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Broadcom, VideoCore VI Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Broadcom, VideoCore VII Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (MediaTek, Mali-G72 OpenGL ES 3.2 vs_5_0 ps_5_0)",
        "ANGLE (MediaTek, Mali-G57 OpenGL ES 3.2 vs_5_0 ps_5_0)",
        "ANGLE (Huawei, Kirin 980 GPU Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Huawei, Kirin 990 GPU Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (ASUS, ROG Phone 3 GPU Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (ASUS, ROG Phone 5 GPU Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Dell, XPS 13 GPU Direct3D11 vs_5_0 ps_5_0)"
    ])

    
    audio_hash = random_hex_string(40)
    client_rects = random_hex_string(40)
    webgpu_report = random_hex_string(40)
    
    # Screen resolution variations
    screen_resolution = random.choice([
        "1920x1080", 
        "1366x768", 
        "2560x1440", 
        "3840x2160", 
        "1280x720", 
        "1440x900",
        "1600x900",
        "1680x1050",
        "1024x768",
        "2560x1600",
        # Add more resolutions as needed
    ])
    
    # Updated Available Screen Sizes as tuples
    available_screen_sizes = [
        (1536, 816), 
        (1280, 720), 
        (2048, 1152), 
        (1920, 1080), 
        (1440, 810),
        (1600, 900),
        (1680, 1050),
        (1024, 768),
        (2560, 1600),
        # Add more available sizes as needed
    ]
    
    available_screen_size = random.choice(available_screen_sizes)
    available_screen_width, available_screen_height = available_screen_size
    
    color_depth = random.choice([24, 32])
    touch_support = random.choice(["Unsupported", "Supported"])
    device_memory = random.choice([4, 8, 16, 32, 64])
    hardware_concurrency = random.choice([2, 4, 6, 8, 16, 32])
    user_agent = random.choice(user_agents)
    
    return {
        "Visitor ID": visitor_id,
        "Canvas": canvas_hash,
        "WebGL": webgl_hash,
        "WebGL Report": webgl_report,
        "Unmasked Vendor": unmasked_vendor,
        "Unmasked Renderer": unmasked_renderer,
        "Audio": audio_hash,
        "Client Rects": client_rects,
        "WebGPU Report": webgpu_report,
        "Screen Resolution": screen_resolution,
        "Available Screen Width": available_screen_width,   # New Field
        "Available Screen Height": available_screen_height, # New Field
        "Color Depth": color_depth,
        "Touch Support": touch_support,
        "Device Memory (GB)": device_memory,
        "Hardware Concurrency": hardware_concurrency,
        "User Agent": user_agent
    }

def generate_fingerprints(num_devices):
    """Generates a list of hardware fingerprints."""
    user_agents = get_user_agents()
    return [generate_fingerprint(user_agents) for _ in range(num_devices)]

def save_to_csv(fingerprints, filename):
    """Saves the list of fingerprints to a CSV file."""
    if not fingerprints:
        print("No fingerprints to save.")
        return
    
    # Define the CSV headers based on the keys of the first fingerprint
    headers = fingerprints[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for fingerprint in fingerprints:
            writer.writerow(fingerprint)
    
    print(f"Successfully saved {len(fingerprints)} fingerprints to '{filename}'.")

if __name__ == "__main__":
    NUM_DEVICES = 500  # You can adjust this number as needed
    OUTPUT_FILE = 'random_devices.csv'
    
    print(f"Generating {NUM_DEVICES} random hardware fingerprints...")
    fingerprints = generate_fingerprints(NUM_DEVICES)
    
    print("Saving fingerprints to CSV...")
    save_to_csv(fingerprints, OUTPUT_FILE)
    
    print("Done!")
