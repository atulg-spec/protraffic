from django.shortcuts import render
from .models import *
from django.utils import timezone
from django.http import JsonResponse
from protraffic.settings import MEDIA_ROOT

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
        campaign_time = 0
        task.repetition_done = task.repetition_done + 1
        task.save()
        campaign = task.campaign
        proxiyOb = Proxy.objects.filter(campaign=task.campaign).filter(status='GOOD')[:task.profile]
        proxies = []
        pages_with_sequence = CampaignPage.objects.filter(campaign=campaign).order_by('sequence')
        # Prepare the pages list in the desired format
        pages_data = [{
            'sequence': page.sequence,
            'scroll_duration_from': page.page.scroll_duration_from,
            'scroll_duration_to': page.page.scroll_duration_to,  # Replace 'name' with actual field names
            'click_selector': page.page.click_selector,  # Replace 'name' with actual field names
            'is_iframe': page.page.is_iframe,  # Replace 'name' with actual field names
        } for page in pages_with_sequence]
        for x in pages_data:
            campaign_time = campaign_time + x['scroll_duration_to']
        campaign_time = campaign_time + (task.profile_delay * task.profile) 
        if task.facebook_campaign:
            campaign_time = campaign_time + (40 * task.profile_delay)
        user_agents = []
        for x in campaign.user_agents.all():
            ob = User_agents.objects.filter(chrome_version=x)
            for y in ob:
                user_agents.append({'userAgents':y.user_agent,'width':y.width,'height':y.height,'isMobile':y.isMobile})
        if proxiyOb:
            proxies = {proxy.proxy:proxy.timezone for proxy in proxiyOb}
            for x in proxiyOb:
                # pass
                x.delete()
        keywords = campaign.keywords.split(',')
        urls = []
        if task.facebook_campaign:
            urls = campaign.urls.split(',')
        elif campaign.direct_traffic:
            urls = campaign.direct_urls.split(',')
        else:
            se = [s.engine for s in campaign.search_engines.all()]
            print(se)
            if 'Google' in se:
                urls = urls + [f'https://www.google.com/search?q={keyword}' for keyword in keywords]
            if 'Yahoo' in se:
                urls = urls + [f'https://search.yahoo.com/search?p={keyword}' for keyword in keywords]
            if 'Bing' in se:
                urls = urls + [f'https://www.bing.com/search?q={keyword}' for keyword in keywords]
            if 'Duck Duck Go' in se:
                urls = urls + [f'https://duckduckgo.com/?q={keyword}' for keyword in keywords]
        campaign_data = {
            'id': campaign.id,
            'created_at': campaign.created_at.strftime('%Y-%m-%d %H:%M:%S') if campaign.created_at else None,
            'campaign_name': campaign.campaign_name,
            'facebook_campaign': task.facebook_campaign,
            'domain_name': campaign.domain_name,
            'facebook_post_div': campaign.facebook_post_div,
            'facebook_ads_div': campaign.facebook_ads_div,
            'is_iframe': campaign.is_iframe,
            'urls': urls,
            'click_anywhere': campaign.click_anywhere,
            'mainurls': campaign.urls.split(','),
            'keywords': campaign.keywords,
            'repetition_count': task.repetition_count,
            'visit_count_from': campaign.visit_count_from,
            'visit_count_to': campaign.visit_count_to,
            'selection_on_page': campaign.selection_on_page,
            'count': proxies.__len__(),
            'profile_delay': task.profile_delay,
            'pages':pages_data,
            'proxies': proxies,
            'campaign_time': campaign_time,
            'cookies_folder': campaign.cookies_folder,
            'user_agents': user_agents,
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

from django.http import FileResponse
import os

def download_zip(request):
    file_path = os.path.join(MEDIA_ROOT, 'WebRTC-Leak-Prevent.zip')
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="WebRTC-Leak-Prevent.zip"'
    return response
