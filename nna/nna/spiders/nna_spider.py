import scrapy
#from inline_requests import inline_requests
#from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class Guardian(scrapy.Spider):
    name = "news1"
    
    start_urls = [
        'https://guardian.ng/'
    ]
    
    def parse(self, response):
        all_news = response.css('.title-latest .item')
        for news in all_news:
            news_url = news.css('.headline .title a::attr("href")')[0].get()
            yield scrapy.Request(news_url, callback=self.parse_news)
            
    def parse_news(self, response):
        yield {
           'title': response.css('.article-header .title::text').get(),
           'link': response.url,
           'imageLink': response.css(' img::attr("data-lazy-src")').get() or response.css('p > img::attr("data-lazy-src")').get(),
           'excerpt': response.css('.article-header .excerpt .excerpt::text').get().strip(),
           'date_posted': response.css('.article-header .subhead div .date::text').get().strip(),
           'site':'Guardian'
        }
        
class Dailypost(scrapy.Spider):
    name = "news2"
    
    start_urls = [
        'https://dailypost.ng/'
    ]
    
    def parse(self, response):
        all_news = response.css('#recent-posts-2 li')
        for news in all_news:
            news_url = news.css('a::attr("href")')[0].get()
            yield scrapy.Request(news_url, callback=self.parse_news)
            
    def parse_news(self, response):
        yield {
            'title': response.css('#mvp-post-head > h1::text').get(),
            'link': response.url,
            'imageLink': response.css('#mvp-post-feat-img > img::attr("src")').get(),
            'excerpt': response.css('#mvp-content-main > p:nth-child(3)').get(),
           'date_posted': response.css('#mvp-post-head > div > div.mvp-author-info-text.left.relative > div.mvp-author-info-date.left.relative > span > time::text').get().strip(),
           'site':'Dailypost'
        }
        
class Premiumtimes(scrapy.Spider):
    name = "news3"
    
    start_urls = [
        'https://www.premiumtimesng.com/'
    ]
    
    def parse(self, response):
        all_news = response.css('.jeg_block_container .jeg_posts article')
        i = 0
        for news in all_news:
            news_url = news.css('.jeg_postblock_content h3 a::attr("href")')[0].get()
            yield scrapy.Request(news_url, callback=self.parse_news)
            if i == 10:
                break
            i+=1
            
    def parse_news(self, response):
        yield {
            'title': response.css('body > div.jeg_viewport > div.post-wrapper > div.post-wrap > div.jeg_main.jeg_sidebar_none > div > div > div > div.row > div > div > div.entry-header > h1::text').get(),
           'link': response.url,
             'imageLink': response.css('body > div.jeg_viewport > div.post-wrapper > div.post-wrap > div.jeg_main.jeg_sidebar_none > div > div > div > div.jeg_featured.featured_image > a > div > img::attr("src")').get(),
            'excerpt': " ".join(response.css('body > div.jeg_viewport > div.post-wrapper > div.post-wrap > div.jeg_main.jeg_sidebar_none > div > div > div > div.row > div > div > div.entry-content.no-share > div.content-inner > p:nth-child(3)::text').extract()),
          'date_posted': response.css('body > div.jeg_viewport > div.post-wrapper > div.post-wrap > div.jeg_main.jeg_sidebar_none > div > div > div > div.row > div > div > div.entry-header > div > div > div.meta_left > div.jeg_meta_date > a::text').get().strip(),
           'site':'Premium Times'
        }
        
class Legit(scrapy.Spider):
    name = "news4"
    
    start_urls = [
        'https://www.legit.ng/latest/'
    ]
    
    def parse(self, response):
        all_news = response.css('section .js-articles article')
        for news in all_news:
            news_url = news.css('.c-article-card-horizontal__container > a::attr("href")')[0].get()
            print(news_url)
            yield scrapy.Request(news_url, callback=self.parse_news)
            
    def parse_news(self, response):
        yield {
            'title': response.css('body > div.l-main-content.js-main-content > div > div.l-adv-branding > div.c-adv-branding__content > section > section > article > header > h1::text').get(),
          'link': response.url,
           'imageLink': response.css('body > div.l-main-content.js-main-content > div > div.l-adv-branding > div.c-adv-branding__content > section > section > article > div.post__content > figure > img::attr("src")').get(),
            'excerpt': response.css('body > div.l-main-content.js-main-content > div > div.l-adv-branding > div.c-adv-branding__content > section > section > article > div.post__content > p:nth-child(3)::text').get(),
           'date_posted': response.css('body > div.l-main-content.js-main-content > div > div.l-adv-branding > div.c-adv-branding__content > section > section > article > header > div.c-article-info.post__info > time::text').get().strip(),
           'site':'LegitNews'
        }
        
class Naija(scrapy.Spider):
    name = "news5"
    
    start_urls = [
        'https://www.naijanews.com/'
    ]
    
    def parse(self, response):
        all_news = response.css('.mvp-main-blog-in div ul .mvp-blog-story-wrap')
        i = 0
        for news in all_news:
            news_url = news.css('a::attr("href")')[0].get()
            yield scrapy.Request(news_url, callback=self.parse_news)
            if i == 10:
                break
            i+=1
            
    def parse_news(self, response):
        yield {
             'title': response.css('#mvp-post-head > h1::text').get(),
           'link': response.url,
           'imageLink': response.css('#mvp-post-feat-img > picture > img::attr("data-src")').get() or response.xpath('//*[@id="mvp-post-feat-img"]/img'),
           'excerpt': response.css('#mvp-content-main > h2::text').get(),
           'date_posted': response.css('#mvp-post-head > div > div > div.mvp-author-info-date.left.relative > p > span > time::text').get().strip(),
           'site':'NaijaNews'
        }
    
class Channel(scrapy.Spider):
    name = "news6"
    
    start_urls = [
        'https://www.channelstv.com/'
    ]
    
    def parse(self, response):
        all_news = response.css('.in-the-news-container .news-list-item')
        i = 0
        for news in all_news:
            news_url = news.css('a::attr("href")')[0].get()
            yield scrapy.Request(news_url, callback=self.parse_news)
            if i == 10:
                break
            i+=1
            
    def parse_news(self, response):
        yield {
             'title': response.css('body > div:nth-child(4) > div.grid_panel > div > div > div:nth-child(2) > div > h2::text').get(),
            'link': response.url,
            'imagelink': response.css('img::attr("src")').extract()[-1],
            'excerpt': response.css('#africa > div > div.col-xs-12.col-sm-12.col-md-7.col-lg-7 > div:nth-child(1) > div.col-lg-12 > p:nth-child(3) > strong').get(),
            'date_posted': response.css('body > div:nth-child(4) > div.grid_panel > div > div > div.post-attribute > div > div.col-sm-6.col-md-8.col-lg-5 > div > div::text').extract()[2].replace("Updated"," ").strip(),
           'site':'ChannelsTV'
        }         

class Independent(scrapy.Spider):
    name = "news7"
    
    start_urls = [
        'https://independent.ng/'
    ]
    
    def parse(self, response):
        all_news = response.css('.bs-listing .listing  article')
        i = 0
        for news in all_news:
            news_url = news.css('div h2 a::attr("href")')[0].get()
            yield scrapy.Request(news_url, callback=self.parse_news)
            if i == 10:
                break
            i+=1
            
    def parse_news(self, response):
        yield {
            'title': response.css('div.post-header.post-tp-1-header > h1 > span::text').get(),
            'link': response.url,
            'imageLink': response.css('div.post-header.post-tp-1-header > div.single-featured > a > img::attr("src")').get(),
            'excerpt': response.css('div.entry-content.clearfix.single-post-content > p:nth-child(3)::text').get(),
           'date_posted': response.css('div.post-header.post-tp-1-header > div.post-meta-wrap.clearfix > div.post-meta.single-post-meta > span > time > b::text').get(),
           'site':'Independent'
        }

class Tribune(scrapy.Spider):
    name = "news8"
    
    start_urls = [
        'https://tribuneonlineng.com/'
    ]
    
    def parse(self, response):
        all_news = response.css('div div article')
        i = 0
        for news in all_news:
            news_url = news.css('div h2 a::attr("href")')[0].get()
            yield scrapy.Request(news_url, callback=self.parse_news)
            if i == 10:
                break
            i+=1
            
    def parse_news(self, response):
        yield {
             'title': response.css('div.post-header.post-tp-1-header > h1 > span::text').get(),
            'link': response.url,
            'imageLink': response.css('div.post-header.post-tp-1-header > div.single-featured > a > img::attr("data-src")').get() or response.css('div.post-header.post-tp-1-header > div.single-featured > a > img::attr("data-src")').extract_first(),
             'excerpt': response.css('div.entry-content.clearfix.single-post-content > *:nth-child(2)::text').get() or response.css('div.entry-content.clearfix.single-post-content > * > span::text').get(),
            'date_posted': response.css('div.post-header.post-tp-1-header > div.post-meta-wrap.clearfix > div.post-meta.single-post-meta > span > time > b::text').get().strip(),
           'site':'Tribune'
        }

class Leadership(scrapy.Spider):
    name = "news9"
    
    start_urls = [
        'https://leadership.ng/'
    ]
    
    def parse(self, response):
        all_news = response.css('.jeg_block_container .jeg_posts div article')
        i = 0
        for news in all_news:
            news_url = news.css('div h3 a::attr("href")')[0].get()
            yield scrapy.Request(news_url, callback=self.parse_news)
            if i == 10:
                break
            i+=1
            
    def parse_news(self, response):
        yield {
          'title': response.css('body > div.jeg_viewport > div.post-wrapper > div.post-wrap > div.jeg_main > div > div > div > div.row > div.jeg_main_content.col-md-8 > div > div.entry-header > h1::text').get(),
           'link': response.url,
           'imageLink': response.css('body > div.jeg_viewport > div.post-wrapper > div.post-wrap > div.jeg_main > div > div > div > div.row > div.jeg_main_content.col-md-8 > div > div.jeg_featured.featured_image > a > div > img::attr("src")').get(),
          'excerpt': response.css('body > div.jeg_viewport > div.post-wrapper > div.post-wrap > div.jeg_main > div > div > div > div.row > div.jeg_main_content.col-md-8 > div > div.entry-content.no-share > div.content-inner > p:nth-child(1)::text').get() or response.css('body > div.jeg_viewport > div.post-wrapper > div.post-wrap > div.jeg_main > div > div > div > div.row > div.jeg_main_content.col-md-8 > div > div.entry-content.no-share > div.content-inner > p:nth-child(1) > span::text').get(),
          'date_posted': response.css('body > div.jeg_viewport > div.post-wrapper > div.post-wrap > div.jeg_main > div > div > div > div.row > div.jeg_main_content.col-md-8 > div > div.entry-header > div > div > div.meta_left > div.jeg_meta_date > a::text').get().strip(),
           'site':'Leadership'
        }

class TheWill(scrapy.Spider):
    name = "news10"
    
    start_urls = [
        'https://thewillnigeria.com/news/'
    ]
    
    def parse(self, response):
        all_news = response.css('.td_module_6 .td-module-thumb')
        i = 0
        for news in all_news:
            news_url = news.css('a::attr("href")')[0].get()
            yield scrapy.Request(news_url, callback=self.parse_news)
            if i == 10:
                break
            i+=1
            
            
    def parse_news(self, response):
        yield {
             'title': response.css('div.td-post-header > header > h1::text').get(),
             'link': response.url,
             'imageLink': response.css('div.td-post-content > div.td-post-featured-image > figure > img::attr("src")').get(),
             'excerpt': response.css('div.td-post-content > p:nth-child(4)::text').get(),
            'date_posted': response.css('div.td-post-header > header > div > span > time::text').get().strip(),
           'site':'TheWill'
        }

settings = get_project_settings()
settings['FEED_FORMAT'] = 'json'
settings['FEED_URI'] = 'news.json'
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
