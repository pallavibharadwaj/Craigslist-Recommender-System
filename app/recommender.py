from pyspark.sql import SparkSession, types
from pyspark.sql.functions import to_json, col, struct
from cassandra.cluster import Cluster

#cluster_seeds = ['199.60.17.32']
cluster_seeds = ['127.0.0.1']
spark = SparkSession.builder.appName('Spark Cassandra example').config('spark.cassandra.connection.host', ','.join(cluster_seeds)).getOrCreate()
assert spark.version>='2.4'
spark.sparkContext.setLogLevel('WARN')

cluster = Cluster(['127.0.0.1'])
keyspace = "potatobytes"
session = cluster.connect(keyspace)

class ListingData:
    def getAllFavorites(self):
        listings = spark.read.format("org.apache.spark.sql.cassandra") \
           .options(table='craigslistcanada', keyspace='potatobytes').load()
        favorites = spark.read.format("org.apache.spark.sql.cassandra") \
            .options(table='favorites', keyspace='potatobytes').load()

        # get all user's favorites
        listings.createOrReplaceTempView('listings')
        favorites.createOrReplaceTempView('favorites')
        favorites = spark.sql("SELECT l.* from listings as l \
                    WHERE l.postingid IN (SELECT DISTINCT postingid FROM favorites WHERE userid='potato')")

        resp = favorites.rdd.collect()
        return resp