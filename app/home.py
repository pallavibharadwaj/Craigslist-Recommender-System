import sys,json
import re,string, datetime
from pyspark.sql import SparkSession, types
from pyspark.sql.functions import to_json, col, struct
from cassandra.cluster import Cluster


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

# load only 20 posts at a time
next_postings = session.prepare('SELECT * FROM %s WHERE token(postingid) > token(?) AND city=? LIMIT 20 ALLOW FILTERING' % craigslist_table)
prev_postings = session.prepare('SELECT * FROM %s WHERE token(postingid) < token(?) AND city=? LIMIT 20 ALLOW FILTERING' % craigslist_table)
next_postings_beds = session.prepare('SELECT * FROM %s WHERE token(postingid) > token(?) AND city=? AND beds=? LIMIT 20 ALLOW FILTERING' % craigslist_table)
prev_postings_beds = session.prepare('SELECT * FROM %s WHERE token(postingid) < token(?) AND city=? AND beds=? LIMIT 20 ALLOW FILTERING' % craigslist_table)

insert_favorite = session.prepare('INSERT INTO %s (userid, postingid) VALUES (?,?)' % fav_table)
delete_favorite = session.prepare('DELETE FROM %s WHERE userid=? AND postingid=? IF EXISTS' % fav_table)
select_favorite = session.prepare('SELECT * from %s WHERE userid=? AND postingid=? ALLOW FILTERING' %fav_table)
truncate_favorite = session.prepare('truncate %s.%s' % (keyspace, fav_table))

select_fav_city = session.prepare('SELECT city FROM %s WHERE postingid=?'%craigslist_table)
select_postid = session.prepare('SELECT * FROM %s'%fav_table)


class ListingData:
    def getAllListings(self, city, beds, last_post):
        if(city is None):
            city='surrey'
        city = city.lower()

        if(last_post == 'first'):   # On first page load
            if (beds is None):
                listings = session.execute(next_postings, ['', city])
            else:
                listings = session.execute(next_postings_beds, ['', city, float(beds)])   
        else:   # Next or Prev button is clicked 
            args = last_post.split('_')
            if(beds is None):
                if(args[0]=='next'):
                    listings = session.execute(next_postings, [args[1], city])
                else:
                    listings = session.execute(prev_postings, [args[1], city])
            else:
                if(args[0]=='next'):
                    listings = session.execute(next_postings_beds, [args[1], city, float(beds)])
                else:
                    listings = session.execute(prev_postings_beds, [args[1], city, float(beds)])

        # get all favorites to show favorited items on reload
        fav = spark.read.format("org.apache.spark.sql.cassandra") \
           .options(table=fav_table, keyspace=keyspace).load()
        fav = fav.rdd.collect()
        
        resp = {
            'listings': list(listings),
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
                fav_city_rows = session.execute(select_fav_city,[fav_postingid])
                fav_city = fav_city_rows[0][0]
                city_rows = session.execute(select_fav_city, [postingid])
                city = city_rows[0][0]
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
