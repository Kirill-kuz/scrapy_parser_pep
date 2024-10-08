import scrapy
import re
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains, start_urls = (
        ['peps.python.org'],
        ['https://peps.python.org/'])

    def parse(self, response):
        all_peps = response.xpath(
            '//a[@class="pep reference internal"]/@href'
        ).getall()
        for pep_link in all_peps:
            yield response.follow(
                pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get()
        parts = re.split('PEP | – ', title)
        number = parts[1].strip()
        name = ' '.join(parts[2:]).strip()

        data = {
            'number': number,
            'name': name,
            'status': response.css(
                'dt:contains("Status")+dd abbr::text'
            ).get(),
        }
        yield PepParseItem(data)
