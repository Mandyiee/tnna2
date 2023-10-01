from celery import shared_task
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from nna.nna.spiders.nna_spider import *
import json,csv

@shared_task
def populate_task():
    settings = get_project_settings()
    settings['FEED_FORMAT'] = 'jsonl'
    settings['FEED_URI'] = 'news.jsonl'
    process = CrawlerProcess(settings)
    process.crawl(Naija)
    process.crawl(Channel)
    process.crawl(Legit)
    process.crawl(Premiumtimes)
    process.crawl(Dailypost)
    process.crawl(Guardian)
    process.crawl(Independent)
    process.crawl(Tribune)
    process.crawl(Leadership)
    process.crawl(TheWill)
    process.start() 
    data = []

    
    with open('news.jsonl', 'r') as jsonl_input:
        for line in jsonl_input:
            data.append(json.loads(line))

    # Write the list of dictionaries to the JSON file
    with open('news.json', 'w') as json_output:
        json.dump(data, json_output, indent=4)