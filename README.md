# craigslist-recommendation-system #

## Getting started ##

![alt text](https://csil-git1.cs.surrey.sfu.ca/potato-bytes/craigslist-recommendation-system/blob/3b56a081829f797a7bfea8628e54bce753d420f5/DFDBD.png)

![alt text](DFDBD.png)
Prerequsites to run the script:
```
1. Root user privilege
2. git
3. pip3
```

Installation:
```
source ./INSTALL.sh
```

### Crawler (SKIP if using the available crawled data) ###

How to Run (generates data/canada.json):

```
python3 crawler/crawler/spiders/craigslist_spider.py
```

### Dumping scraped data to Cassandra ###

Create the required keyspace ("potatobytes"):
```
CREATE KEYSPACE potatobytes WITH REPLICATION = {
'class': 'SimpleStrategy', 'replication_factor': 1 };
```

To populate the scraped listings from the JSON file into the Cassandra database:
```
spark-submit data/load_cassandra.py data/canada.json
```

### Web Application ###

How to Run:
```
python3 app/app.py
```

In Browser (Tested on Firefox):
```
http://localhost:5000/
```
