# craigslist-recommendation-system

## Getting started

### CRAWLER ###

Required dependencies and packages:

```
sudo apt-get install python3-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev libxslt-dev libxml2-dev1
pip3 install scrapy
pip3 install scrapy_useragents
pip3 install scrapy-rotating-proxies
```

How to Run:

```
cd ~/craigslist-recommendation-system/crawler/crawler/spiders/
python3 craigslist_spider.py
```

### Web Application ###

How to Run:

```
cd ~/craigslist-recommendation-system/app
python3 app.py
```
In the browser type 
```
localhost:5000/
```

### Database ###

To populate the scraped listings from the JSON file into the Cassandra database, assuming keyspace and table are already created in Cassandra, run:

```
cd ~/craigslist-recommendation-system/data
python3 add --packages datastax:spark-cassandra-connector:2.4.0-s_2.11 load_cassandra.py canada.json
```

