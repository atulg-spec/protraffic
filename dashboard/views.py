from django.shortcuts import render
from .models import *
from django.utils import timezone
from django.http import JsonResponse
import datetime

# Create your views here.
def getcampaigns(request,user):
    usr = User.objects.get(username=user)
    task = Tasks.objects.filter(user=usr,status="created").first()    
    if task is None:
        return JsonResponse({'status':False,'data':{}}, safe=False)
    # Serialize campaigns data
    campaign_data = {}
    now = timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone())  # Get current datetime in Asia/Kolkata
    if task.schedule_at <= now:
        campaign = task.campaign
        proxiyOb = Proxy.objects.filter(campaign=task.campaign)
        proxies = []
        user_agents = []
        for x in campaign.user_agents.all():
            ob = User_agents.objects.filter(chrome_version=x)
            for y in ob:
                user_agents.append(y.user_agent)
        if proxiyOb:
            proxies = [proxy.proxy for proxy in proxiyOb]
        keywords = campaign.keywords.split(',')
        urls = [f'https://www.google.com/search?q={keyword}' for keyword in keywords]
        cook = Cookies.objects.filter(campaign=campaign)
        cookies = [c.json_data for c in cook]
        campaign_data = {
            'id': campaign.id,
            'created_at': campaign.created_at.strftime('%Y-%m-%d %H:%M:%S') if campaign.created_at else None,
            'campaign_name': campaign.campaign_name,
            'domain_name': campaign.domain_name,
            'time_zone': campaign.time_zone,
            'extension_path': campaign.extension_path,
            'urls': urls,
            'keywords': campaign.keywords,
            'search_engines': campaign.search_engines,
            'repetition_count': task.repetition_count,
            'visit_count_from': campaign.visit_count_from,
            'visit_count_to': campaign.visit_count_to,
            'count': task.count,
            'scroll_duration': campaign.scroll_duration,
            'proxies': proxies,
            'user_agents': user_agents,
            'cookies': cookies,
        }
    
    # Return JSON response
    return JsonResponse({'status':True,'data':campaign_data}, safe=False)


def repetitiondone(request,id):
    try:
        ob = Campaigns.objects.filter(id=id).first() 
        ob.repetition_done = ob.repetition_done + 1
        ob.save()
    except:
        pass
    return JsonResponse({'status':True})