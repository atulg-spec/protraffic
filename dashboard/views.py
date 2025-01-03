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
        task.repetition_done = task.repetition_done + 1
        task.save()
        campaign = task.campaign
        proxies = []
        user_agents = []
        for x in campaign.user_agents.all():
            ob = User_agents.objects.filter(chrome_version=x)
            for y in ob:
                user_agents.append(
                    {
                        'userAgents':y.user_agent,
                        'width':y.width,
                        'height':y.height,
                        'visitor_id':y.visitor_id,
                        'canvas':y.canvas,
                        'WebGL':y.WebGL,
                        'WebGL_report':y.WebGL_report,
                        'unmasked_renderer':y.unmasked_renderer,
                        'audio':y.audio,
                        'client_rects':y.client_rects,
                        'webGPU_report':y.webGPU_report,
                        'screen_resolution':y.screen_resolution,
                        'color_depth':y.color_depth,
                        'touch_support':y.touch_support,
                        'device_memory':y.device_memory,
                        'hardware_concurrency':y.hardware_concurrency,
                        'isMobile':y.isMobile
                    }
                    )
        proxiyOb = Proxy.objects.filter(campaign=task.campaign).filter(status='GOOD')[:task.profile]
        if proxiyOb:
            proxies = {proxy.proxy:proxy.timezone for proxy in proxiyOb}
            for x in proxiyOb:
                # pass
                x.delete()
        if task.make_google_logins:
            from youtube.models import EmailAccounts
            accountsob = EmailAccounts.objects.filter(tag=campaign.profiles_tag)
            accounts = []
            if accountsob:
                accounts = [{'email':x.email,'password':x.password} for x in accountsob]
            campaign_data = {
                'id': campaign.id,
                'campaign_name': campaign.campaign_name,
                'accounts': accounts,
                'make_google_logins': task.make_google_logins,
                'facebook_campaign': False,
                'profile_delay': task.profile_delay,
                'proxies': proxies,
                'cookies_folder': campaign.cookies_folder,
                'user_agents': user_agents,
            }
            # Return JSON response
            return JsonResponse({'status':True,'data':campaign_data}, safe=False)
        elif task.youtube_subscribe:
            campaign_data = {
                'id': campaign.id,
                'campaign_name': campaign.campaign_name,
                'profileTag': f'{campaign.profiles_tag}',
                'urls': campaign.urls.split(','),
                'youtube_subscribe': task.youtube_subscribe,
                'make_google_logins': False,
                'facebook_campaign': False,
                'profile_delay': task.profile_delay,
                'proxies': proxies,
                'cookies_folder': campaign.cookies_folder,
                'user_agents': user_agents,
            }
            # Return JSON response
            return JsonResponse({'status':True,'data':campaign_data}, safe=False)
        elif task.youtube_views:
            pages_with_sequence = CampaignPage.objects.filter(campaign=campaign).order_by('sequence')
            # Prepare the pages list in the desired format
            pages_data = [{
                'sequence': page.sequence,
                'scroll_duration_from': page.page.scroll_duration_from,
                'scroll_duration_to': page.page.scroll_duration_to,  # Replace 'name' with actual field names
                'click_selector': page.page.click_selector,  # Replace 'name' with actual field names
                'is_iframe': page.page.is_iframe,  # Replace 'name' with actual field names
            } for page in pages_with_sequence]
            campaign_data = {
                'id': campaign.id,
                'campaign_name': campaign.campaign_name,
                'pages': pages_data,
                'profileTag': f'{campaign.profiles_tag}',
                'urls': campaign.urls.split(','),
                'youtube_views': task.youtube_views,
                'youtube_subscribe': False,
                'make_google_logins': False,
                'facebook_campaign': False,
                'profile_delay': task.profile_delay,
                'proxies': proxies,
                'cookies_folder': campaign.cookies_folder,
                'user_agents': user_agents,
            }
            # Return JSON response
            return JsonResponse({'status':True,'data':campaign_data}, safe=False)
        elif task.create_google_accounts:
            pages_with_sequence = CampaignPage.objects.filter(campaign=campaign).order_by('sequence')
            # Prepare the pages list in the desired format
            pages_data = [{
                'sequence': page.sequence,
                'scroll_duration_from': page.page.scroll_duration_from,
                'scroll_duration_to': page.page.scroll_duration_to,  # Replace 'name' with actual field names
                'click_selector': page.page.click_selector,  # Replace 'name' with actual field names
                'is_iframe': page.page.is_iframe,  # Replace 'name' with actual field names
            } for page in pages_with_sequence]
            campaign_data = {
                'id': campaign.id,
                'campaign_name': campaign.campaign_name,
                'pages': pages_data,
                'profileTag': f'{campaign.profiles_tag}',
                'urls': campaign.urls.split(','),
                'create_google_accounts': task.create_google_accounts,
                'youtube_views': False,
                'youtube_subscribe': False,
                'make_google_logins': False,
                'facebook_campaign': False,
                'profile_delay': task.profile_delay,
                'proxies': proxies,
                'cookies_folder': campaign.cookies_folder,
                'user_agents': user_agents,
            }
            # Return JSON response
            return JsonResponse({'status':True,'data':campaign_data}, safe=False)
        else:
            campaign_time = (10 * task.profile) + 60
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
                'direct_traffic': campaign.direct_traffic,
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
