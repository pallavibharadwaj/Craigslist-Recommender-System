import sys,json
import re,string
from pyspark.sql import SparkSession, types
from pyspark.sql.functions import to_json, col, struct

#cluster_seeds = ['199.60.17.32']
cluster_seeds = ['127.0.0.1']
spark = SparkSession.builder.appName('Spark Cassandra example').config('spark.cassandra.connection.host', ','.join(cluster_seeds)).getOrCreate()
assert spark.version>='2.4'
spark.sparkContext.setLogLevel('WARN')
spark.conf.set("spark.sql.session.timeZone", "GMT")

class ListingData:
    def getAllListings(self):
        df = spark.read.format("org.apache.spark.sql.cassandra") \
           .options(table='craigslistcanada', keyspace='potatobytes').load()

        df.createOrReplaceTempView('df')
        resp = spark.sql("SELECT postingid, baths, beds, url, position, price, labels, title, city FROM df WHERE city='Halifax'").rdd.collect()

        return resp
