from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import zipfile
import json

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
    

class User_agents(models.Model):
    id = models.AutoField(primary_key=True)
    chrome_version = models.ForeignKey(Chrome_versions, on_delete=models.CASCADE)
    user_agent = models.CharField(max_length=200,default="")

    class Meta:
        unique_together = ('chrome_version', 'user_agent')
        verbose_name = "User Agent"
        verbose_name_plural = "User Agents"

    def __str__(self):
        return f'{self.user_agent}'


class Campaigns(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    campaign_name = models.CharField(max_length=50, default="")
    domain_name = models.CharField(max_length=50, default="")
    time_zone = models.CharField(max_length=50, default="America/New_York")
    user_agents = models.ManyToManyField(Chrome_versions)
    extension_path = models.CharField(max_length=100, default="C:/Users/atulg/Desktop/WebRTC-Leak-Prevent")
    urls = models.TextField(default="")
    keywords = models.TextField(default="")
    facebook_urls = models.TextField(default="",null=True,blank=True)
    search_engines = models.CharField(max_length=100, choices=SEARCH_ENGINES, default="Google")
    repetition_count = models.PositiveIntegerField(default=1)
    repetition_done = models.PositiveIntegerField(default=0)
    visit_count_from = models.PositiveIntegerField(default=1)
    visit_count_to = models.PositiveIntegerField(default=1)
    count = models.PositiveIntegerField(default=3)
    from_time = models.PositiveIntegerField(default=1)
    to_time = models.PositiveIntegerField(default=3)
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
        self.add_cookies_from_zip()
        if is_new and self.proxy_file:
            self.add_proxies_from_file()

                    

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

    def __str__(self):
        return f'{self.campaign.campaign_name} - {self.proxy}'

class CookieFile(models.Model):
    campaign = models.ForeignKey(Campaigns, on_delete=models.CASCADE, related_name='cookie_files', default=1)  # Set a default campaign ID
    file = models.FileField(upload_to='cookies/')

    class Meta:
        verbose_name = "Cookie File"
        verbose_name_plural = "Cookie Files"

    def __str__(self):
        return self.file.name


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    campaign = models.ForeignKey(Campaigns, on_delete=models.CASCADE, related_name='tasks')
    schedule_at = models.DateTimeField()
    status = models.CharField(max_length=100, choices=STATUS, default="created")

    class Meta:
        unique_together = ('campaign', 'schedule_at')
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return f'{self.campaign.campaign_name} - at {self.schedule_at}'


