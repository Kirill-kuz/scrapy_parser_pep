import scrapy

from pep_parse.items import PepParseItem
import re


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = [
        f'https://{domain}/' for domain in allowed_domains]

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
