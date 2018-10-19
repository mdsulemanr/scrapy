# -*- coding: utf-8 -*-
import scrapy


class LoginSpiderSpider(scrapy.Spider):
    name = 'login-spider'
    login_url = 'http://quotes.toscrape.com/login'
    start_urls = [login_url]

    def parse(self, response):
        token = response.css('input[name="csrf_token"]::attr(value)').extract_first()
        data = {
            'csrf_token' : token,
            'username' : 'abc',
            'password' : 'abc'
        }
        # yield a post request
        yield scrapy.FormRequest(url=self.login_url, formdata=data, callback=self.parse_quotes)

    def parse_quotes(self, response):
        for quote in response.css('div.quote'):
            yield {'author_name': quote.css('small.author::text').extract_first(),
                   'author_url' : quote.css('small.author ~ a[href*="goodreads.com"]::attr(href)').extract_first()
                    }

        next_page = response.css('li.next > a::attr(href)').extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
        yield scrapy.Request(url=next_page, callback=self.parse_quotes)
