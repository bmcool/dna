#-*- encoding: utf-8 -*-

import re

from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from collection.items import DjangoItem
from dna.models import Movie

class Spider(BaseSpider):
    name = "movie"
    allowed_domains = ["atmovies.com.tw"]
    start_urls = ['http://app.atmovies.com.tw/atmdb/atmdb.cfm?action=filmyear']
    url_schema = "http://app.atmovies.com.tw/"
    
    def parse(self, response):
        print response.body
        # for subjectModel in self.sourceModel.subject_set.filter(enabled=True):
            # title = subjectModel.title
            # link = subjectModel.link
            
            # subjectModel.delta_time = get_subject_delta_time(subjectModel, datetime.timedelta(days = subjectModel.day))
            # subjectModel.last_modified_time = self.now - subjectModel.delta_time
            
            # log.msg("[Subject] Crawl [" + title + "]", level=log.INFO)
            
            # request = Request(link, callback = self.parse_articles)
            # request.meta['subjectModel'] = subjectModel
            
            # yield request
    
    def parse_articles(self, response):
        hxs = HtmlXPathSelector(response)
        subjectModel = response.meta['subjectModel']
        
        current_page, total_page = get_page_number_info(hxs)
        
        articles = hxs.select('//td[@class="subject"]')
        next = False
        for article in articles:
            last_modified_time_string = ''.join(article.select('following-sibling::td[@class="latestreply"]/a/p[1]/text()').extract())
            last_modified_time = datestring_to_datetime(last_modified_time_string)
            
            published_time_string = ''.join(article.select('following-sibling::td[@class="authur"]/a/p[1]/text()').extract())
            published_time = datestring_to_datetime(published_time_string)
            
            reply_count = ''.join(article.select('following-sibling::td[@class="reply"]/text()').extract())
            reply_count = int(re.sub(',', '', reply_count))
            
            if subjectModel.last_modified_time < last_modified_time:
                next = True
            
            topic = article.select('span/a')
            url = ''.join(topic.select('@href').extract())
            link = urljoin(self.url_schema, url)
            original_id = re.findall('t=(\d+)', url)[0]
            popularity = ''.join(topic.select('@title').extract())
            popularity = int(re.findall('(\d+)$', popularity)[0])
            
            request = Request(link, callback = self.get_article_reply)
            request.meta['articleOriginalID'] = original_id
            request.meta['articlePublishedTime'] = published_time
            request.meta['subjectModel'] = subjectModel
            request.meta['reply_count'] = reply_count
            request.meta['popularity'] = popularity
            
            yield request
        
        log.msg("[Subject] In [" + subjectModel.title + "] page " + str(current_page), level=log.INFO)
        if current_page < total_page and next == True:
            request = Request(response.url + "&p=" + str(current_page + 1), callback = self.parse_articles)
            request.meta['subjectModel'] = subjectModel
            
            yield request
    
    def get_article_reply(self, response):
        hxs = HtmlXPathSelector(response)
        articleOriginalID = response.meta['articleOriginalID']
        articlePublishedTime = response.meta['articlePublishedTime']
        subjectModel = response.meta['subjectModel']
        reply_count = response.meta['reply_count']
        popularity = response.meta['popularity']
        
        title = ''.join(hxs.select('//h2[@class="topic"]/text()').extract())
        if title:
            articleModel, created = subjectModel.article_set.get_or_create(original_id=articleOriginalID)
            articleModel.published_time = articlePublishedTime
            articleModel.title = title
            articleModel.reply_count = reply_count
            articleModel.popularity = popularity
            articleItem = DjangoItem(django_model=articleModel)
            yield articleItem
            
            current_page, total_page = get_page_number_info(hxs)
            log.msg("[Article] In [" + subjectModel.title + "]/[" + articleModel.title + "] page " + str(current_page), level=log.INFO)
            count = 0
            for article in hxs.select('//div[@class="single-post"]'):
                original_id, author_name, content, last_modified_time = get_content_info(article)
                
                if current_page == 1 and count == 0:
                    model = articleModel
                else:
                    model, created = articleModel.reply_set.get_or_create(original_id=original_id)
                    log.msg("[Reply] In [" + subjectModel.title + "]/[" + articleModel.title + "] page " + str(current_page) + "\n" + content, level=log.DEBUG)
                    if not model.published_time:
                        model.published_time = last_modified_time
                
                model.popularity = popularity
                model.link = response.url + "#" + original_id
                model.author = author_name
                model.content = content
                modelItem = DjangoItem(django_model=model)
                yield modelItem
                
                count += 1
            
            if total_page > 1:
                # p=999999 for the newest page
                request = Request(response.url + "&p=999999", callback = self.get_reply)
                request.meta['articleModel'] = articleModel
                request.meta['subjectModel'] = subjectModel
                request.meta['popularity'] = popularity
                
                yield request
    
    def get_reply(self, response):
        articleModel = response.meta['articleModel']
        subjectModel = response.meta['subjectModel']
        popularity = response.meta['popularity']
        
        link = re.findall('(.+)&p=\d+', response.url)[0]
        
        hxs = HtmlXPathSelector(response)
        
        current_page, total_page = get_page_number_info(hxs)
        
        articles = hxs.select('//div[@class="single-post"]')
        next = False
        total_length = len(articles)
        for i in range(0, total_length):
            article = articles.pop()
            original_id, author_name, content, last_modified_time = get_content_info(article)
            
            if subjectModel.last_modified_time < last_modified_time:
                next = True
            
            replyModel, created = articleModel.reply_set.get_or_create(original_id=original_id)
            replyModel.author = author_name
            replyModel.popularity = popularity
            replyModel.link = link + "&p=" + str(current_page) + "#" + original_id
            replyModel.content = content
            if not replyModel.published_time:
                replyModel.published_time = last_modified_time
            
            replyItem = DjangoItem(django_model=replyModel)
            yield replyItem
        
        log.msg("[Reply] In [" + subjectModel.title + "]/[" + articleModel.title + "] page " + str(current_page) + "\n" + content, level=log.DEBUG)
        if current_page > 2 and next == True:
            request = Request(link + "&p=" + str(current_page - 1), callback = self.get_reply)
            request.meta['articleModel'] = articleModel
            request.meta['subjectModel'] = subjectModel
            request.meta['popularity'] = popularity
            
            yield request
        