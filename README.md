# craigslist-recommendation-system

## Getting started

### Crawler ###

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

### Cassandra ###

To populate the scraped listings from the JSON file into the Cassandra database, assuming keyspace and table are already created in Cassandra, run:

```
cd ~/craigslist-recommendation-system/data
spark-submit --packages datastax:spark-cassandra-connector:2.4.0-s_2.11 load_cassandra.py canada.json
```

### Web Application ###

Required dependencies and packages:

```
pip3 install flask
pip3 install flask-cors
```
How to Run:

```
cd ~/craigslist-recommendation-system/app
python3 app.py
```
In Browser:

```
http://localhost:5000/
```
