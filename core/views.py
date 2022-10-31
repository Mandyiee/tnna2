import pprint
from django.shortcuts import render
from django.http import JsonResponse
import subprocess,os,json
from pathlib import Path

# Create your views here.
def index(request):
    path = Path.cwd()
    os.chdir(Path.home())
    modifiedPath = os.path.join(path,'nna/nna')
    modifiedPath = Path(modifiedPath)
    os.chdir(modifiedPath)
    filepath = 'news.json'
    if os.path.exists(Path(os.path.join(Path.cwd(),filepath))):  
        os.remove(filepath)
   
    f = open(filepath,'r')
    data = f.read()
    print(data)
    modifiedData = pprint.pformat(data)
    os.chdir(path) 
    return JsonResponse(data,safe=False)


#Path(os.path.join(modifiedPath,'news.json'))