# -*- coding: utf-8 -*-
import scrapy


class RipucSpider(scrapy.Spider):
    name = 'ripuc'
    allowed_domains = ['ripuc.org']
    start_urls = ['http://www.ripuc.org/eventsactions/docket.html']

    def row_data(self, row, docket_talbe):
        docket = row.xpath('td[1]/a/text()|td[1]/text()').extract()
        filer = row.xpath('td[2]/p/text()|td[2]/text()').extract()
        description = row.xpath('td[3]/p/text()|td[3]/span/text()|td[3]/text()').extract()
        return docket, filer, description

    def parse(self, response):
        docket_talbe = response.xpath('//td[@class="normal"]/table')
        same_filer = 0
        same_description = 0
        for row in docket_talbe.xpath('tr')[1:]:
            # Unique Docket, Filer and Description
            if row.xpath('count(td)=3 and not(td[1][@rowspan="2"]) and not(td[2][@rowspan="2"])').extract_first()=='1':
                docket, filer, description = self.row_data(row, docket_talbe)

            # Dependent Docket and unique Filer and Description
            elif row.xpath('count(td)=3 and td[1][@rowspan="2"]').extract_first()=='1':
                docket, filer, description = self.row_data(row, docket_talbe)

                if row.xpath('boolean(td[2][@rowspan="2"])').extract_first()=='1':
                    same_filer = 1
                if row.xpath('boolean(td[3][@rowspan="2"])').extract_first()=='1':
                    same_description=1

            elif row.xpath('count(td)=3 and not(td[1][@rowspan="2"]) and td[2][@rowspan="2"]').extract_first() == '1':
                docket, filer, description = self.row_data(row, docket_talbe)
                if row.xpath('boolean(td[2][@rowspan="2"])').extract_first() == '1':
                    same_filer = 1

            elif row.xpath('count(td)=2 and not(td[1]/a[contains(@href, "docket")])').extract_first()=='1':
                filer = row.xpath('td[1]/p/text()|td[1]/text()').extract()
                description = row.xpath('td[2]/p/text()|td[2]/span/text()|td[2]/text()').extract()

            elif row.xpath('count(td)=2 and td[1]/a[contains(@href, "docket")]').extract_first()=='1':
                if same_filer==1:
                    docket = row.xpath('td[1]/a/text()|td[1]/text()').extract()
                    description = row.xpath('td[2]/text()').extract_first()
                    same_filer = 0

            else:
                if row.xpath('count(td)=1').extract_first()=='1':
                    if same_description == 1:
                        filer = row.xpath('td[1]/p/text()|td[1]/text()').extract()
                        same_description = 0

                    if same_filer == 1:
                        description = row.xpath('td[1]/text()').extract_first()
                        same_filer = 0
            item = {
                'docket': docket,
                'filer': filer,
                'description': description
            }
            yield item