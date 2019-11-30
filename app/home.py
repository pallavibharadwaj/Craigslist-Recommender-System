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
spark.conf.set("spark.sql.session.timeZone", "UTC")

cluster = Cluster(['127.0.0.1'])
keyspace = "potatobytes"
session = cluster.connect(keyspace)

fav_table = "favorites"
craigslist_table = "craigslistcanada"
insert_favorite = session.prepare('INSERT INTO %s (userid, postingid) VALUES (?,?)' % fav_table)
delete_favorite = session.prepare('DELETE FROM %s WHERE userid=? AND postingid=? IF EXISTS' % fav_table)
select_favorite = session.prepare('SELECT * from %s WHERE userid=? AND postingid=? ALLOW FILTERING' %fav_table)
truncate_favorite = session.prepare('truncate potatobytes.favorites')

select_fav_city = session.prepare('SELECT city FROM %s WHERE postingid=?'%craigslist_table)
select_postid = session.prepare('SELECT * FROM %s'%fav_table)


class ListingData:
    def getAllListings(self,city):
        print('city: ',city)
        df_all = spark.read.format("org.apache.spark.sql.cassandra") \
            .options(table='craigslistcanada', keyspace='potatobytes').load()
        city_upper = city.upper()
        city_caps = city.capitalize()
        data = df_all.where((df_all['city']==city) | (df_all['city']==city_upper) | (df_all['city']==city_caps))
        d = data.rdd.collect()
        #data.createOrReplaceTempView('df')
        #listings = spark.sql("SELECT * FROM df WHERE city='%s'" % city).rdd.collect()

        fav = spark.read.format("org.apache.spark.sql.cassandra") \
           .options(table='favorites', keyspace='potatobytes').load()
        fav = fav.rdd.collect()
        
        resp = {
            'listings': d, #listings
            'favorites': fav
        }
        return resp

    def add_favorite(self, postingid):
        resp = {}
        row  = ['potato', postingid]
        try: 
            fav_rows = session.execute(select_postid)
            if(fav_rows):
                fav_postingid=fav_rows[0][1]            
                print('fav_postingid inside first if: ',fav_postingid, type(fav_postingid))
                fav_city_rows = session.execute(select_fav_city,[fav_postingid])
                fav_city = fav_city_rows[0][0]
                print('city within fav table: ',fav_city)
                city_rows = session.execute(select_fav_city, [postingid])
                city = city_rows[0][0]
                print('city from current listing: ',city)
                if fav_city==city:
                    if(session.execute(select_favorite, row)):  # delete if already in favorites
                        session.execute(delete_favorite, row)
                    else:   # insert favorite
                        session.execute(insert_favorite, row)
                else:
                    session.execute(truncate_favorite)
                    session.execute(insert_favorite,row)
            else:
                session.execute(insert_favorite,row)        
        except:
            resp = {'error': 'Could not favorite the listing, please try again later'}
        
        return resp
