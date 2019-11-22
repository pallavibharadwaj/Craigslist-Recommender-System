import scrapy
import os, json
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

#
# Spider1 - crawl and fetch 100 elite proxy IPs
#
class ProxySpider(scrapy.Spider):
    name="proxy"

    def start_requests(self):
        urls = [
            'https://www.sslproxies.org/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        outfile = "proxies.txt"
        os.system("rm -f %s" % outfile)

        tr = response.css('table[id="proxylisttable"] tbody tr')

        for row in tr:
            # proxy - IP:PORT
            proxy = row.css('td::text').getall()[0]+":"+row.css('td::text').getall()[1]

            with open(outfile, 'a+') as f:
                f.write(proxy+"\n")

#
# Spider2 - fetch all Craigslist Posts
#
class CraigslistSpider(scrapy.Spider):
    name = "craigslist"

    def start_requests(self):
        urls = [
            'https://www.craigslist.org/about/sites'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_canada_url)

    def parse_canada_url(self,response):
        # scrape each region in Canada domain
        for region in response.css('div.colmask a::attr(href)').re(r'https://\w*\.\w*\.ca'):
            yield scrapy.Request(url=region+"/search/apa", callback=self.parse) 

    def parse(self, response):
        # scrape each post in the page
        for post in response.css('li.result-row a::attr(href)').re(r'https://.*'):
            yield response.follow(post, callback=self.parse_post)

        if(response.css('a.button.next::attr(href)').re(r'\?s=[\d]+')):
            next_page = response.css('a.button.next::attr(href)').re(r'\?s=[\d]+')[0]   # query string

            # loop through all the pages following the next button
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

    def parse_post(self, response):
        attributes = response.css('p.attrgroup:nth-child(n+3) span::text').getall()
        labels = {}
        for attr in attributes:
            if(attr.lstrip()):  # chuck empty labels
                labels[attr] = 1
        fields = {
            'postingid': response.css('p.postinginfo::text').re(r'(\d+)')[0] if response.css('p.postinginfo::text').re(r'(\d+)') else None,
            'region': response.css('meta[name="geo.region"]::attr(content)').get() or None,
            'city': response.css('meta[name="geo.placename"]::attr(content)').get() or None,
            'position': response.css('meta[name="geo.position"]::attr(content)').get() or None,
            'url': response.css('meta[property="og:url"]::attr(content)').get() or None,
            'title': response.css('meta[property="og:title"]::attr(content)').get() or None,
            'image': response.css('meta[property="og:image"]::attr(content)').get() or None,
            'posted': response.css('time::attr(datetime)').get() or None,
            'price': response.css('span.price::text').get() or None,
            'beds': float(response.css('b::text').re(r'(\d*\.?\d*)BR')[0]) if response.css('b::text').re(r'(\d*\.?\d*)BR') else None,
            'baths': float(response.css('b::text').re(r'(\d*\.?\d*)Ba')[0]) if response.css('b::text').re(r'(\d*\.?\d*)Ba') else None,
            'labels': labels
        }
        outfile = "../../../data/canada.json"
        if(fields['postingid']):
            with open(outfile, 'a') as f:
                json.dump(fields, f)
                f.write("\n")

configure_logging()
#
# run spiders sequentially
#
runner = CrawlerRunner()
@defer.inlineCallbacks

def crawl():
    yield runner.crawl(ProxySpider)

    # use the modified project settings
    runner.settings=get_project_settings()

    yield runner.crawl(CraigslistSpider)

    reactor.stop()

crawl()
reactor.run()
