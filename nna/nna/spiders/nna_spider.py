import scrapy
from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import datetime
import re
#scrapy crawl news7 -o output.jsonl -a append=True
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
           'imageLink': response.css('div > img::attr("src")').get(),
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
            'excerpt': response.css('#mvp-content-main > p:nth-child(3)').get() or response.xpath('//*[@id="mvp-content-main"]/p[1]/text()').get(),
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
        date_posted = response.css('body > div.jeg_viewport > div.post-wrapper > div.post-wrap > div.jeg_main > div > div > div > div.row > div.jeg_main_content.col-md-8 > div > div.entry-header > div > div > div.meta_left > div.jeg_meta_date > a::text').get()
    
        if date_posted != 'null' and date_posted != None:
            date_posted = date_posted.strip() 
        else:
            date_posted = datetime.date.today().strftime("%d %B %Y")

        yield {
             'title': response.css('#mvp-post-head > h1::text').get() or response.xpath('/html/body/div[2]/div[2]/div/div[1]/article/div/div/div/header/h1/text()').get(),
           'link': response.url,
           'imageLink': response.css('#mvp_home_feat2_widget-3 > div > div.mvp-widget-feat2-wrap.left.relative > div > div.mvp-widget-feat2-side.left.relative > div > div > a:nth-child(2) > div > div > div.mvp-feat1-list-img.left.relative > img::attr("data-src")').get() or response.xpath('//*[@id="mvp-post-feat-img"]/img/@data-src').get(),
           'excerpt': response.xpath('//*[@id="mvp-content-main"]/h2/text()[2]').get() or response.xpath('//*[@id="mvp-content-main"]/p[1]/text()').get() or response.xpath('//*[@id="mvp-content-main"]/h2/text()[1]').get(),
           'date_posted': date_posted,
           'site':'NaijaNews'
        }
    
class Channel(scrapy.Spider):
    name = "news6"
    
    start_urls = [
        'https://www.channelstv.com/'
    ]
    
    def parse(self, response):
        all_news = response.css('body > main > section.site-sections.headlines.top_stories > div > div.article_wrapper > div > div > div > div.col-lg-4.g-lg-3 > div > article:nth-child(1) > div > div > div > h3')
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
            'imagelink': response.css('img::attr("src")').get()[-1],
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
        all_news = response.css('body > div.jeg_viewport > div.elementor.elementor-692147 > section.elementor-section.elementor-top-section.elementor-element.elementor-element-dc0536f.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div.elementor-column.elementor-col-33.elementor-top-column.elementor-element.elementor-element-499792fd > div > div > div > div > div.jeg_block_container > div.jeg_posts > div > article')
        i = 0
        for news in all_news:
            news_url = news.css('div > h3 > a::attr("href")')[0].get()
            yield scrapy.Request(news_url, callback=self.parse_news)
            if i == 10:
                break
            i+=1
            
    def parse_news(self, response):
        date_posted = response.css('body > div.jeg_viewport > div.post-wrapper > div.post-wrap > div.jeg_main > div > div > div > div.row > div.jeg_main_content.col-md-8 > div > div.entry-header > div > div > div.meta_left > div.jeg_meta_date > a::text').get()
           
        if date_posted != 'null' and date_posted != None:
            date_posted = date_posted.strip() 
        else:
            date_posted = datetime.date.today().strftime("%d %B %Y")
        yield {
             'title': response.css('body > div.jeg_viewport > div.post-wrapper > div.post-wrap > div.jeg_main > div > div > div > div.row > div.jeg_main_content.col-md-8 > div > div.entry-header > h1::text').get(),
            'link': response.url,
            'imageLink': response.css('body > div.jeg_viewport > div.post-wrapper > div.post-wrap > div.jeg_main > div > div > div > div.row > div.jeg_main_content.col-md-8 > div > div.jeg_featured.featured_image > a > div > img::attr("data-src")').get() or response.css('body > div.jeg_viewport > div.post-wrapper > div.post-wrap > div.jeg_main > div > div > div > div.row > div.jeg_main_content.col-md-8 > div > div.jeg_featured.featured_image > a > div > img::attr("src")').extract_first(),
             'excerpt':  response.xpath('//div[@class="entry-content no-share"]/p/text()').get() or response.css('div.entry-content.no-share p::text').get(),
            'date_posted': date_posted,
           'site':'Tribune'
        }

class Leadership(scrapy.Spider):
    #scrapy crawl news9 -o output.json -a append=True

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
        date_posted = response.css('body > div.jeg_viewport > div.post-wrapper > div.post-wrap > div.jeg_main > div > div > div > div.row > div.jeg_main_content.col-md-8 > div > div.entry-header > div > div > div.meta_left > div.jeg_meta_date > a::text').get()
    
        if date_posted != 'null' and date_posted != None:
            date_posted = date_posted.strip() 
        else:
            date_posted = datetime.date.today().strftime("%d %B %Y")
            
        yield {
          'title': response.css('body > div.jeg_viewport > div.post-wrapper > div.post-wrap > div.jeg_main.jeg_wide_content > div > div > div > div.row > div.jeg_main_content.col-md-9 > div > div.entry-header > h1::text').get(),
           'link': response.url,
           'imageLink': response.css('body > div.jeg_viewport > div.post-wrapper > div.post-wrap > div.jeg_main.jeg_wide_content > div > div > div > div.row > div.jeg_main_content.col-md-9 > div > div.jeg_featured.featured_image > a > div > img::attr("src")').get(),
          'excerpt': response.xpath('/html/body/div[2]/div[5]/div[1]/div[1]/div/div/div/div[2]/div[1]/div/div[5]/div[2]/p[2]/text()[1]').get(),
          'date_posted': date_posted,
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
        date_posted = response.css('div.td-post-header > header > div > span > time::text').get()
        if date_posted != 'null' and date_posted != None:
            date_posted = date_posted.strip() 
        else:
            date_posted = datetime.date.today().strftime("%d %B %Y")
        image_css =  response.css('#tdi_63 > div > div.vc_column.tdi_66.wpb_column.vc_column_container.tdc-column.td-pb-span8 > div > div.vc_row_inner.tdi_68.vc_row.vc_inner.wpb_row.td-pb-row > div > div > div > div.td_block_wrap.tdb_single_bg_featured_image.tdi_72.tdb-content-horiz-center.td-pb-border-top.td_block_template_1 > style:nth-child(2)').get()
        pattern = r"background:url\('([^']+)'"
        image_matches = re.findall(pattern, image_css)
        image = response.css('div.td-post-content > div.td-post-featured-image > figure > img::attr("src")').get()
        if image_matches:
            image = image_matches[0]
        yield {
             'title': response.css('#tdi_63 > div > div.vc_column.tdi_66.wpb_column.vc_column_container.tdc-column.td-pb-span8 > div > div.vc_row_inner.tdi_68.vc_row.vc_inner.wpb_row.td-pb-row > div > div > div > div.td_block_wrap.tdb_breadcrumbs.tdi_71.td-pb-border-top.td_block_template_1.tdb-breadcrumbs > div > span.tdb-bred-no-url-last::text').get(),
             'link': response.url,
             'imageLink': image,
             'excerpt': response.xpath('//*[@id="tdi_63"]/div/div[1]/div/div[4]/div/p[1]/text()').get(),
            'date_posted': date_posted,
           'site':'TheWill'
        }

# settings = get_project_settings()
# settings['FEED_FORMAT'] = 'jsonl'
# settings['FEED_URI'] = 'news.jsonl'
# process = CrawlerProcess(settings)
# process.crawl(Naija)#
# process.crawl(Channel)
# process.crawl(Legit)#
# process.crawl(Premiumtimes)#
# process.crawl(Dailypost)#
# process.crawl(Guardian)#
# process.crawl(Independent)#
# process.crawl(Tribune)
# process.crawl(Leadership)#
# process.crawl(TheWill)
# process.start() 
