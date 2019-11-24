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

Required dependencies and packages:
* spark-cassandra-connector:
```
git clone https://github.com/datastax/spark-cassandra-connector.git
cd spark-cassandra-connector
./sbt/sbt assembly -Dscala-2.11=true
cp ~/spark-cassandra-connector/spark-cassandra-connector/target/full/scala-2.11/spark-cassandra-connector-assembly-2.4.1-28-g29e31d3.jar $SPARK_HOME/jars/
```

To populate the scraped listings from the JSON file into the Cassandra database:

```
cd ~/craigslist-recommendation-system/data
spark-submit load_cassandra.py canada.json <keyspace> <table-name>
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
