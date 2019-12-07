
# craigslist-recommendation-system #

## Getting started ##

Prerequsites to run the script:
```
1. Root user privilege
2. git
3. pip3
```

## Installation ##
```
source ./INSTALL.sh
```
### Alternate Installation(If Spark and Cassandra already exists) ###
Step 1: To update to the latest version of the packages

```
apt-get update
```

Step 2: To install scrapy on Ubuntu (or Ubuntu-based) systems, you need to install these dependencies:

```
apt-get install -y python3-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev libxslt-dev libxml2-dev
```

Step 3: To install java openjdk

```
apt-get -y install openjdk-8-jdk --fix-missing
```

Step 4: To install all required python packages

```
pip3 install -r requirements.txt
```

Step 5: To install the spark-cassandra-connector:

```
git clone https://github.com/datastax/spark-cassandra-connector.git
cd spark-cassandra-connector/ && sbt/sbt assembly -Dscala-2.11=true
cp spark-cassandra-connector/spark-cassandra-connector/target/full/scala-2.11/spark-cassandra-connector-assembly-2.4.2-3-gda707460.jar $SPARK_HOME/jars/
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

