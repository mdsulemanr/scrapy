# -*- coding: utf-8 -*-
import scrapy


class RipucSpider(scrapy.Spider):
    name = 'ripuc'
    allowed_domains = ['ripuc.org']
    start_urls = ['http://www.ripuc.org/eventsactions/docket.html']

    def parse(self, response):
        table = response.xpath('//td[@class="normal"]/table')
        number_of_rows = int(float(table.xpath('count(tr)').extract_first()))

        for i in range(2, number_of_rows+1):
            if table.xpath('tr[{}]/td[@rowspan="2"][1]/a/text()'.format(i)).extract():
                docket = table.xpath('tr[{}]/td[@rowspan="2"][1]/a/text()'.format(i)).extract()

                if table.xpath('tr[{}]/td[2]/p/text()'.format(i)).extract():
                    filer = table.xpath('tr[{}]/td[2]/p/text()'.format(i)).extract()
                else:
                    filer= table.xpath('tr[{}]/td[2]/text()'.format(i)).extract()

                if table.xpath('tr[{}]/td[3]/p/text()'.format(i)).extract():
                    description = table.xpath('tr[{}]/td[3]/p/text()'.format(i)).extract()
                else:
                    description = table.xpath('tr[{}]/td[3]/text()'.format(i)).extract()

                item = {
                'docket' : docket,
                'filer' : filer,
                'description' : description
                }
                yield item

                if table.xpath('tr[{}]/td[2]'.format(i+1)).extract_first():
                    if table.xpath('tr[{}]/td[1]/p/text()'.format(i+1)).extract():
                        filer1 = table.xpath('tr[{}]/td[1]/p/text()'.format(i+1)).extract()
                    else:
                        filer1 = table.xpath('tr[{}]/td[1]/text()'.format(i+1)).extract()

                    if table.xpath('tr[{}]/td[2]/p/text()'.format(i+1)).extract():
                        description1 = table.xpath('tr[{}]/td[2]/p/text()'.format(i+1)).extract()
                    else:
                        description1 = table.xpath('tr[{}]/td[2]/text()'.format(i + 1)).extract()

                    item = {
                    'docket' : docket,
                    'filer' : filer1,
                    'description' : description1
                    }
                    yield item

                else:
                    if table.xpath('tr[{}]/td[@rowspan="2"][3]'.format(i)).extract_first():
                        item = {
                        'docket': docket,
                        'filer': filer1,
                        'description': description
                        }
                        yield item

                    else:
                        description2 = table.xpath('tr[{}]/td[1]/text()'.format(i+1)).extract_first()
                        item = {
                        'docket': docket,
                        'filer': filer,
                        'description': description2
                        }
                        yield item
            else:
                if table.xpath('tr[{}]/td[3]'.format(i)).extract():
                    if table.xpath('tr[{}]/td[1]/a/text()'.format(i)).extract():
                        docket = table.xpath('tr[{}]/td[1]/a/text()'.format(i)).extract()
                    else:
                        docket = table.xpath('tr[{}]/td[1]/text()'.format(i)).extract()

                    if table.xpath('tr[{}]/td[2]/p/text()'.format(i)).extract():
                        filer = table.xpath('tr[{}]/td[2]/p/text()'.format(i)).extract()
                    else:
                        filer= table.xpath('tr[{}]/td[2]/text()'.format(i)).extract()

                    if table.xpath('tr[{}]/td[3]/p/text()'.format(i)).extract():
                        description = table.xpath('tr[{}]/td[3]/p/text()'.format(i)).extract()
                    elif table.xpath('tr[{}]/td[3]/span/text()'.format(i)).extract():
                        description = table.xpath('tr[{}]/td[3]/span/text()'.format(i)).extract()
                    else:
                        description = table.xpath('tr[{}]/td[3]/text()'.format(i)).extract()

                    item = {
                    'docket' : docket,
                    'filer' : filer,
                    'description' : description
                    }
                    yield item
