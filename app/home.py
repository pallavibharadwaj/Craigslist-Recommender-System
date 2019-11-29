import sys,json
import re,string, datetime
from pyspark.sql import SparkSession, types
from pyspark.sql.functions import to_json, col, struct
from cassandra.cluster import Cluster

#cluster_seeds = ['199.60.17.32']
cluster_seeds = ['127.0.0.1']
spark = SparkSession.builder.appName('Spark Cassandra example').config('spark.cassandra.connection.host', ','.join(cluster_seeds)).getOrCreate()
assert spark.version>='2.4'
spark.sparkContext.setLogLevel('WARN')
spark.conf.set("spark.sql.session.timeZone", "GMT")

cluster = Cluster(['127.0.0.1'])
keyspace = "potatobytes"
session = cluster.connect(keyspace)

fav_table = "favorites"
insert_favorite = session.prepare('INSERT INTO %s (userid, postingid) VALUES (?,?)' % fav_table)
delete_favorite = session.prepare('DELETE FROM %s WHERE userid=? AND postingid=? IF EXISTS' % fav_table)
select_favorite = session.prepare('SELECT * from %s WHERE userid=? AND postingid=? ALLOW FILTERING' %fav_table)

class ListingData:
    def getAllListings(self):
        df = spark.read.format("org.apache.spark.sql.cassandra") \
           .options(table='craigslistcanada', keyspace='potatobytes').load()

        df.createOrReplaceTempView('df')
        listings = spark.sql("SELECT * FROM df WHERE city='Halifax'").rdd.collect()

        fav = spark.read.format("org.apache.spark.sql.cassandra") \
           .options(table='favorites', keyspace='potatobytes').load()
        fav = fav.rdd.collect()

        resp = {
            'listings': listings,
            'favorites': fav
        }

        return resp

    def add_favorite(self, postingid):
        resp = {}
        row = ['potato', postingid]
        try:
            if(session.execute(select_favorite, row)):  # delete if already in favorites
                session.execute(delete_favorite, row)
            else:   # insert favorite
                session.execute(insert_favorite, row)

        except:
            resp = {'error': 'Could not favorite the listing, please try again later'}
        
        return resp