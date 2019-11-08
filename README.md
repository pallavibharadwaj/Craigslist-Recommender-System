# craigslist-recommendation-system

### CRAWLER ###

Requirements:

1. pip install Scrapy
2. pip install beautifulsoup4
3. pip install scrapy_useragents
4. pip install scrapy-rotated-proxy


How to Run:

1. Create proxies.txt with a list of 100 elite proxies in the spiders/ folder. These IPs are rotated and used by scrapy to crawl craigslist.

$ cd ~/craigslist-recommendation-system/crawler/crawler/
$ ./proxy_generator.py

2. The crawler generates data in a JSON file. To run the crawler:

$ cd ~/craigslist-recommendation-system/crawler/crawler/spiders/
$ scrapy crawl craigslist
