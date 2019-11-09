import scrapy
import random

class CraigslistSpider(scrapy.Spider):
    name = "craigslist"

    def start_requests(self):
        urls = [
            'https://vancouver.craigslist.org/search/apa'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]

        # scrape each post in the page
        for post in response.css('li.result-row a::attr(href)').re(r'https://.*'):
            yield response.follow(post, callback=self.parse_post)


        next_page = response.css('a.button.next::attr(href)').re(r'\?s=[\d]+')[0]   # query string

        # loop through all the pages following the next button
        if next_page is not None:
            global page_count
            page_count += 1
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_post(self, response):
        attributes = response.css('p.attrgroup:nth-child(n+3) span::text').getall()
        labels = {}
        for attr in attributes:
            labels[attr] = 1
        fields = {
            'posting-id':response.css('p.postinginfo::text').re(r'(\d+)'),
            'region': response.css('meta[name="geo.region"]::attr(content)').get(),
            'city': response.css('meta[name="geo.placename"]::attr(content)').get(),
            'position': response.css('meta[name="geo.position"]::attr(content)').get(),
            'url': response.css('meta[property="og:url"]::attr(content)').get(),
            'title': response.css('meta[property="og:title"]::attr(content)').get(),
            'image': response.css('meta[property="og:image"]::attr(content)').get(),
            'posted': response.css('time::attr(datetime)').get(),
            'price': response.css('span.price::text').get(),
            'beds': response.css('b::text').re(r'(\d\.*\d*)+BR'),
            'baths': response.css('b::text').re(r'(\d\.*\d*)+Ba'),
            'labels': labels
        }
        yield fields

