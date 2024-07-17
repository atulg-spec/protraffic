from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import zipfile
import json
import pytz

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


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


class Campaigns(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    campaign_name = models.CharField(max_length=50, default="")
    domain_name = models.CharField(max_length=50, default="")
    time_zone = models.CharField(max_length=32, choices=TIMEZONES,default='America/New_York')
    user_agents = models.ManyToManyField(Chrome_versions)
    extension_path = models.CharField(max_length=100, default="C:/Users/Administrator/Desktop/WebRTC-Leak-Prevent")
    urls = models.TextField(default="")
    keywords = models.TextField(default="")
    search_engines = models.ManyToManyField(SearchEngine)
    visit_count_from = models.PositiveIntegerField(default=1)
    visit_count_to = models.PositiveIntegerField(default=1)
    scroll_duration = models.PositiveIntegerField(default=30)
    cookies_file = models.FileField(upload_to='cookies_zip/',null=True,blank=True)
    proxy_file = models.FileField(upload_to='proxies/')

    class Meta:
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"

    def __str__(self):
        return self.campaign_name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and self.proxy_file:
            try:
                self.add_cookies_from_zip()
            except:
                pass
            try:
                self.add_proxies_from_file()
            except:
                pass

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

    class Meta:
        unique_together = ('campaign', 'proxy')
        verbose_name = "Proxy"
        verbose_name_plural = "Proxies"

    def save(self, *args, **kwargs):
        if self.proxy[0].isdigit():  # Check if proxy starts with a number
            self.proxy = f'--proxy-server=socks5://{self.proxy}'
        super().save(*args, **kwargs)

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
    count = models.PositiveIntegerField(default=3)
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


