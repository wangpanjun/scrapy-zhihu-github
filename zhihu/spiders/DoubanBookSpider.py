# encoding=utf-8

import re
import json


from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

from zhihu.items import *



class DoubanBookSpider(CrawlSpider):

    name = "douban_book"
    allowed_domains = ["douban.com"]
    start_urls = [
        # "http://book.douban.com/tag/"
        # "http://www.douban.com/"
        'http://www.douban.com/tag/小说/book'
    ]
    a = 0
    rules = (
        Rule(LinkExtractor(allow=r'^http://book.douban.com/tag/$'), callback='parse_tag'),
        Rule(LinkExtractor(allow='\?start=\d*'),callback='parse_list', follow=True),
        Rule(LinkExtractor(allow='/subject/\d*/\?from=tag_all'),callback='parse_list1'),
    )

    def parse_tag(self, response):
        print "d"
        # sel = Selector(response)
        # tags = sel.xpath('//table[@class="tagCol"]/tbody/tr/td/a/text()').extract()
        #
        # # for tag in tags[0:1]:
        # url = "http://www.douban.com/tag/%s/book" % tags[0]
        # yield Request(url, callback=self.parse_list)

    def parse_list(self,response):
        self.a += 1
        print self.a
        # print response.body
        # sel = Selector(response)
        # dls = sel.xpath('//div[@class="mod book-list"]/dl')
        # for dl in dls:
        #     book = DouBookItem()
        #     book["url"]= dl.xpath('dt/a/@href').extract()[0]
        #     book["name"] = dl.xpath('dd/a/text()').extract()[0]
        #     book["desc"] = dl.xpath('dd/div[@class="desc"]/text()').extract()[0]
        #     book["rating"] = dl.xpath('dd/div[@class="rating"]/span[@class="rating_nums"]/text()').extract()[0]
        #     yield book

    def parse_list1(self, response):
        print "1"*100
    # rules = [
    #     # Rule(LinkExtractor(allow=("http://book.douban.com/subject/\d+/?$")), callback='parse_2'),
    #     # Rule(LinkExtractor(allow=("/tag/[^/]+/?$", )), follow=True),
    #     # Rule(LinkExtractor(allow=("/tag/\w*/\?$focus=book", )), callback='parse_1'),
    #     # Rule(LinkExtractor(allow=("/tag/[\u4E00-\u9FFF]*·?[\u4E00-\u9FFF]*/\?focus=book", )),
    #     #      callback='parse_1'),http://book.douban.com/subject/10546125/?from=tag
    #     # Rule(LinkExtractor(allow=("/tag/[\x00-\xff]*/\?focus=book", )),callback='parse_1'),%E6%B2%A7%E6%9C%88/
    #     Rule(LinkExtractor(allow=("/tag/小说/\?focus=book", )),callback='parse_1'),
    #     Rule(LinkExtractor(allow=("/subject/\d*/\?focus=tag", )),callback='_process_request'),
    #     ]

    def parse_2(self, response):
        print '3'*100
        items = []
        sel = Selector(response)
        sites = sel.css('#wrapper')
        for site in sites:
            item = DoubanSubjectItem()
            item['title'] = site.css('h1 span::text').extract()
            item['link'] = response.url
            item['content_intro'] = site.css('#link-report .intro p::text').extract()
            items.append(item)
            print repr(item).decode("unicode-escape") + '\n'
        # info('parsed ' + str(response))
        return items

    def parse_1(self, response):
        sel = Selector(response)
        dls = sel.xpath('//div[@id="book"]//dl')
        for dl in dls:
            book = DoubanbookItem()
            book["url"] = dl.xpath('dt/a/@href').extract()[0]
            book["img"]  = dl.xpath('dt/a/img/@src').extract()[0]
            book["name"]  = dl.xpath('dd/a/text()').extract()[0]
            book["desc"]  = dl.xpath('dd/div[@class="desc"]/text()').extract()[0]
            book["rating"]  = dl.xpath('dd/div[@class="rating"]/span[@class="rating_nums"]/text()').extract()[0]
            print repr(book).decode("unicode-escape") + '\n'


    def _process_request(self, request):
        print 2
        #info('process ' + str(request))
        # return request

    # def parse(self, response):
    #     print '4'*100
    #     print type(response)



    # def parse_links(self, links):
    #     print "d"*100
    #     newlinks = []
    #
    #     for link in links:
    #         link.url = re.compile('\?ref=.*$').sub('', link.url)
    #         #link.url = link.url.replace('ref','aaaaaaaaaaaaa')
    #         newlinks.append(link)
    #
    #     return newlinks


