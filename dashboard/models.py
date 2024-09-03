from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import zipfile
import json
from multiselectfield import MultiSelectField
import pytz
import threading
import requests

CONTINENTS = {
    'Africa': [],
    'Antarctica': [],
    'Asia': [],
    'Europe': [],
    'North America': [],
    'Oceania': [],
    'South America': []
}

# Populate the CONTINENTS dictionary with timezones
for tz in pytz.all_timezones:
    if tz.startswith('Africa/'):
        CONTINENTS['Africa'].append(tz)
    elif tz.startswith('Antarctica/'):
        CONTINENTS['Antarctica'].append(tz)
    elif tz.startswith('Asia/'):
        CONTINENTS['Asia'].append(tz)
    elif tz.startswith('Europe/'):
        CONTINENTS['Europe'].append(tz)
    elif tz.startswith('America/') and 'Argentina' not in tz and 'Indiana' not in tz:
        if 'South_America' in tz or 'Argentina' in tz:
            CONTINENTS['South America'].append(tz)
        else:
            CONTINENTS['North America'].append(tz)
    elif tz.startswith('Pacific/') or tz.startswith('Australia/') or tz.startswith('Indian/'):
        CONTINENTS['Oceania'].append(tz)

# Create continent choices for Django model
CONTINENT_CHOICES = [(continent, continent) for continent in CONTINENTS.keys()]


SEARCH_ENGINES = [
    ('Google', 'Google'),
    ('Bing', 'Bing'),
    ('Yahoo', 'Yahoo'),
    # Add other search engines if needed
]
STATUS = [
        ('created', 'created'),
        ('working', 'working'),
        ('completed', 'completed'),
    ]

CONDITION = [
        ('FETCHING', 'FETCHING'),
        ('BAD', 'BAD'),
        ('GOOD', 'GOOD'),
    ]


class Chrome_versions(models.Model):
    version = models.CharField(max_length=50)

    class Meta:
        unique_together = ('version',)
        verbose_name = "Chrome Version"
        verbose_name_plural = "Chrome Versions"

    def __str__(self):
        return f'{self.version}'


class SearchEngine(models.Model):
    engine = models.CharField(max_length=50)

    class Meta:
        unique_together = ('engine',)
        verbose_name = "Search Engine"
        verbose_name_plural = "Search Engines"

    def __str__(self):
        return f'{self.engine}'



class User_agents(models.Model):
    id = models.AutoField(primary_key=True)
    chrome_version = models.ForeignKey(Chrome_versions, on_delete=models.CASCADE)
    user_agent = models.CharField(max_length=200,default="")
    width = models.PositiveIntegerField(default=1536)
    height = models.PositiveIntegerField(default=864)
    isMobile = models.BooleanField(default=False)

    class Meta:
        unique_together = ('chrome_version', 'user_agent')
        verbose_name = "User Agent"
        verbose_name_plural = "User Agents"

    def __str__(self):
        return f'{self.user_agent}'

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
TIMEZONE_COUNTRIES = sorted(set([(pytz.country_names[code], pytz.country_names[code]) for code in pytz.country_names]))

class PageBehaviour(models.Model):
    scroll_duration_from = models.PositiveIntegerField(default=10)
    scroll_duration_to = models.PositiveIntegerField(default=30)

    class Meta:
        verbose_name = "Page Behaviour"
        verbose_name_plural = "Pages Behaviours"

    def __str__(self):
        return f'Scroll from {self.scroll_duration_from}-{self.scroll_duration_to}'

class CampaignPage(models.Model):
    campaign = models.ForeignKey('Campaigns', on_delete=models.CASCADE)
    page = models.ForeignKey('PageBehaviour', on_delete=models.CASCADE)
    sequence = models.PositiveIntegerField()  # Represents the order or sequence of the page

    class Meta:
        ordering = ['sequence']  # Ensures pages are retrieved in the correct order
        unique_together = ('campaign', 'sequence')  # Ensures unique sequence number within a campaign


class Campaigns(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    campaign_name = models.CharField(max_length=50, default="")
    domain_name = models.CharField(max_length=50, default="")
    continent = models.CharField(max_length=100, choices=CONTINENT_CHOICES, null=True, blank=True)
    time_zone = MultiSelectField(choices=TIMEZONES, default='America/New_York')
    user_agents = models.ManyToManyField(Chrome_versions)
    facebook_post_div = models.CharField(max_length=200, default="div.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.xtlvy1s.x126k92a")
    facebook_ads_div = models.CharField(max_length=200, default="div.search__result__wrapper")
    extension_path = models.CharField(max_length=100, default="C:/Users/Administrator/Desktop/WebRTC-Leak-Prevent")
    urls = models.TextField(default="")
    keywords = models.TextField(default="")
    search_engines = models.ManyToManyField(SearchEngine)
    visit_count_from = models.PositiveIntegerField(default=1)
    visit_count_to = models.PositiveIntegerField(default=1)
    direct_traffic = models.BooleanField(default=False)
    pages = models.ManyToManyField(PageBehaviour, through='CampaignPage')  # Use the through model
    only_last_page_scroll_for_facebook = models.BooleanField(default=False)
    cookies_file = models.FileField(upload_to='cookies_zip/', null=True, blank=True)
    proxy_file = models.FileField(upload_to='proxies/',null=True,blank=True)

    class Meta:
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"

    def __str__(self):
        return self.campaign_name

    def save(self, *args, **kwargs):
        if self.continent:
            self.time_zone = CONTINENTS.get(self.continent, [])

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            if self.cookies_file:
                try:
                    self.add_cookies_from_zip()
                except Exception as e:
                    raise ValidationError(f"Error saving cookies: {e}")

            if self.proxy_file:
                try:
                    self.add_proxies_from_file()
                except Exception as e:
                    raise ValidationError(f"Error saving proxies: {e}")

    def add_proxies_from_file(self):
        try:
            with transaction.atomic():
                with self.proxy_file.open('r') as f:
                    for line in f:
                        proxy = line.strip()
                        if proxy:
                            Proxy.objects.create(campaign=self, proxy=proxy)
        except Exception as e:
            raise ValidationError(f"Error saving proxies: {e}")

    def add_cookies_from_zip(self):
        try:
            with zipfile.ZipFile(self.cookies_file.path, 'r') as zip_ref:
                for filename in zip_ref.namelist():
                    with zip_ref.open(filename) as json_file:
                        json_data = json.load(json_file)
                        Cookies.objects.create(campaign=self, json_data=json_data)
        except Exception as e:
            raise ValidationError(f"Error saving cookies: {e}")


class Proxy(models.Model):
    campaign = models.ForeignKey(Campaigns, on_delete=models.CASCADE, related_name='proxies')
    proxy = models.CharField(max_length=255)

    # Fields to store IP-related data
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    timezone = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=100, choices=CONDITION, default="FETCHING")

    class Meta:
        unique_together = ('campaign', 'proxy')
        verbose_name = "Proxy"
        verbose_name_plural = "Proxies"

    def save(self, *args, **kwargs):
        # Adjust proxy format if needed
        if ':' in self.proxy:
            parts = self.proxy.split(':')
            if len(parts) == 4:
                self.proxy = f'{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}'

        is_new = self._state.adding  # Check if the instance is newly created

        # Save the model first to ensure the primary key exists
        super().save(*args, **kwargs)

        # Perform the operation in a new thread only if the instance is newly created
        if is_new:
            threading.Thread(target=self.fetch_and_save_ip_details).start()

        # Start a new thread to fetch and save IP details

    def fetch_and_save_ip_details(self):
        proxy = self.proxy
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

            self.ip_address = ip_address
            self.city = city
            self.region = region
            self.country = country
            self.timezone = timezone
            if timezone not in self.campaign.time_zone:
                self.status = 'BAD'
            else:
                self.status = 'GOOD'
            with transaction.atomic():
                self.save(update_fields=['ip_address', 'city', 'region', 'country', 'timezone','status'])

        except requests.exceptions.RequestException as e:
            self.status = 'BAD'
            with transaction.atomic():
                self.save(update_fields=['status'])
            print(f"Error: {e}")

    def __str__(self):
        return f'{self.campaign.campaign_name} - {self.proxy}'


class CookieFile(models.Model):
    campaign = models.ForeignKey(Campaigns, on_delete=models.CASCADE, related_name='cookie_files', default=1)  # Set a default campaign ID
    file = models.FileField(upload_to='cookies/')

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and self.file:
            self.add_cookies_from_zip()

    def add_cookies_from_zip(self):
        try:
            with zipfile.ZipFile(self.file.path, 'r') as zip_ref:
                for filename in zip_ref.namelist():
                    with zip_ref.open(filename) as json_file:
                        json_data = json.load(json_file)
                        Cookies.objects.create(campaign=self.campaign, json_data=json_data)
        except Exception as e:
            raise ValidationError(f"Error saving cookies: {e}")

    class Meta:
        verbose_name = "Cookie Upload"
        verbose_name_plural = "Cookies Upload"

    def __str__(self):
        return self.file.name

class Proxyfile(models.Model):
    campaign = models.ForeignKey('Campaigns', on_delete=models.CASCADE, related_name='proxyfile', default=1)
    proxies = models.TextField(default='', null=True, blank=True)
    file = models.FileField(upload_to='proxies/', blank=True, null=True)    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file:
            self.add_proxies_from_file()
        if self.proxies:
            self.add_proxies_from_input()   
    def add_proxies_from_file(self):
        try:
            with transaction.atomic():
                with self.file.open('r') as f:
                    for line in f:
                        proxy = line.strip()
                        if proxy:
                            Proxy.objects.get_or_create(campaign=self.campaign, proxy=proxy)
        except Exception as e:
            raise ValidationError(f"Error saving proxies from file: {e}")   
    def add_proxies_from_input(self):
        try:
            with transaction.atomic():
                for line in self.proxies.splitlines():
                    proxy = line.strip()
                    if proxy:
                        Proxy.objects.get_or_create(campaign=self.campaign, proxy=proxy)
        except Exception as e:
            raise ValidationError(f"Error saving proxies from input: {e}")  
    class Meta:
        verbose_name = "Proxy Upload"
        verbose_name_plural = "Proxies Upload"  
    def __str__(self):
        return self.file.name if self.file else "Proxy Upload"


class UserAgentsFile(models.Model):
    Chrome_version = models.ForeignKey('Chrome_versions', on_delete=models.CASCADE, related_name='chromeversions', default=1)
    user_agents = models.TextField(default='', null=True, blank=True)
    file = models.FileField(upload_to='useragents/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file:
            self.add_agents_from_file()
        if self.user_agents:
            self.add_agents_from_input()

    def add_agents_from_file(self):
        try:
            with transaction.atomic():
                with self.file.open('r') as f:
                    for line in f:
                        agent = line.strip()
                        if agent:
                            User_agents.objects.get_or_create(chrome_version=self.Chrome_version, user_agent=agent)
        except Exception as e:
            raise ValidationError(f"Error saving User Agents from file: {e}")

    def add_agents_from_input(self):
        try:
            with transaction.atomic():
                for line in self.user_agents.splitlines():
                    agent = line.strip()
                    if agent:
                        User_agents.objects.get_or_create(chrome_version=self.Chrome_version, user_agent=agent)
        except Exception as e:
            raise ValidationError(f"Error saving User Agents from input: {e}")

    class Meta:
        verbose_name = "User Agents Upload"
        verbose_name_plural = "User Agents Upload"

    def __str__(self):
        return self.file.name if self.file else "User Agents Upload"

class Cookies(models.Model):
    campaign = models.ForeignKey(Campaigns, on_delete=models.CASCADE)
    json_data = models.JSONField()

    class Meta:
        verbose_name = "Cookie"
        verbose_name_plural = "Cookies"

    def __str__(self):
        return f"Cookies for {self.campaign.campaign_name}"



class Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ManyToManyField(User)
    repetition_count = models.PositiveIntegerField(default=1)
    repetition_done = models.PositiveIntegerField(default=0)
    profile = models.PositiveIntegerField(default=3)
    profile_delay = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    campaign = models.ForeignKey(Campaigns, on_delete=models.CASCADE, related_name='tasks')
    schedule_at = models.DateTimeField()
    status = models.CharField(max_length=100, choices=STATUS, default="created")
    facebook_campaign = models.BooleanField(default=False)

    class Meta:
        unique_together = ('campaign', 'schedule_at')
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.repetition_count <= self.repetition_done:
            self.status = 'completed'
            super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.campaign.campaign_name} - at {self.schedule_at}'


