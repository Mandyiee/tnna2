import pprint, uuid
from django.shortcuts import render
from django.http import JsonResponse
import subprocess,os
import json, requests, bs4
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.conf import settings
from rest_framework import serializers
# Create your views here.


def index(request):
    try:
        response = []
        res = requests.get('https://guardian.ng/')
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        mainHtml = soup.select('.title-latest')
        sectionHtml = soup.select('.item')
        section = sectionHtml[0]
        mainHeadline = section.select('.headline')
        mainTitle = mainHeadline[0].select('.title')
        mainLinks= mainTitle[0].select('a')
        title = mainLinks[0].getText()
        link = mainLinks[0].get('href')
        obj = { 'title' : title, 'link':link, 'site': 'guardian'}
        mainContent = section.select('.excerpt')
        obj['excerpt'] = mainContent[0].getText()
        mainTime = section.select('.age')
        mainImgLink = section.select('div img')
        obj['imageLink'] = mainImgLink[0].get('data-lazy-src')
        obj['time'] = mainTime[0].getText()
        mobj = {}
        mobj['title'] = obj['title'][:40] + '... '
        mobj['link'] = obj['link'][:40] + '... '
        mobj['excerpt'] = obj['excerpt'][:40] + '... '
        mobj['imageLink'] = obj['imageLink'][:40] + '... '
        mobj['time'] = obj['time']
        context = {
            'obj':obj,
            'mobj': mobj,
        }
    except:
        context = {
            'obj': None,
            'mobj': None,
        }
    return render(request,'index.html',context)

@api_view(['GET'])
def apiIndex(request):
    api_key = request.GET.get('api_key')
    if api_key: 
        try:
            profile = Profile.objects.get(api_key=api_key)
        except Profile.DoesNotExist:
            obj = {
                'Invalid API key': 'your API key is not valid'
            }
            return Response(obj)
        profile.api_count += 1
        profile.save()
        project_path = settings.BASE_DIR
        file_path = os.path.join(project_path, 'news.json')
        
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        return Response(data)
    else:
        obj = {
                'No API key': 'you do have an API key'
            }
        return Response(obj)

#i removed this twisted-iocpsupport==1.0.2 from requirements.txt in oreder for it to work
@login_required(login_url='accounts/login')
def profile(request):
    user = User.objects.get(username=request.user.username)
    
    try:
        profile = Profile.objects.filter(user=user).first()
    except Profile.DoesNotExist:
        profile = None
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'create':
            api_key = uuid.uuid4()  
            profile = Profile.objects.create(user=user,api_key=api_key)
            profile.save()  
        else:
            api_key = uuid.uuid4()  
            profile.api_key = api_key
            profile.save()    
    context = {
        'profile':profile
    }
    
    return render(request,'profile.html',context)

def my_custom_page_not_found_view(request,exception):
    return render(request,'404.html')

def my_custom_bad_request_view(request,exception):
    return render(request,'400.html')

def my_custom_error_view(request):
    return render(request,'500.html')

def my_custom_permission_denied_view(request,exception):
    return render(request,'404.html')


@api_view(['GET'])
@login_required(login_url='accounts/login')
def apiAdmin(request):
    project_path = settings.BASE_DIR
    file_path = os.path.join(project_path, 'news.json')
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return Response(data)

