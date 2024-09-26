import csv
from django.core.management.base import BaseCommand
from dashboard.models import User_agents, Chrome_versions

class Command(BaseCommand):
    help = 'Upload user agents from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Get or create the Chrome version instance
                chrome_version, created = Chrome_versions.objects.get_or_create(
                    version=row.get('User Agent')  # Assuming you have a way to get the version
                )

                is_mobile = False
                if row['Touch Support'] == 'Supported':
                    is_mobile = True
                # Create User_agents instance
                User_agents.objects.create(
                    chrome_version=chrome_version,
                    user_agent=row['User Agent'],
                    visitor_id=row['Visitor ID'],
                    canvas=row['Canvas'],
                    WebGL=row['WebGL'],
                    WebGL_report=row['WebGL Report'],
                    unmasked_vendor=row['Unmasked Vendor'],
                    unmasked_renderer=row['Unmasked Renderer'],
                    audio=row['Audio'],
                    client_rects=row['Client Rects'],
                    webGPU_report=row['WebGPU Report'],
                    screen_resolution=row['Screen Resolution'],
                    width=row.get('Available Screen Width', 1536),  # Default width
                    height=row.get('Available Screen Height', 864),  # Default height
                    color_depth=row['Color Depth'],
                    touch_support=row['Touch Support'],
                    device_memory=row['Device Memory (GB)'],
                    hardware_concurrency=row['Hardware Concurrency'],
                    isMobile=is_mobile  # Convert to boolean
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully added: {row["User Agent"]}'))
