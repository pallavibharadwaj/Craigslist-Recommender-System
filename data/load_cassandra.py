import sys,json
import re,string
import datetime
from pyspark.sql import SparkSession,functions,types
from cassandra.cluster import Cluster

#cluster_seeds = ['199.60.17.32'] #for loading to cluster, in any case
cluster_seeds = ['127.0.0.1']
spark = SparkSession.builder.appName('Data going to Cassandra').config('spark.cassandra.connection.host', ','.join(cluster_seeds)).getOrCreate()
assert spark.version>='2.4'
spark.sparkContext.setLogLevel('WARN')
sc = spark.sparkContext
spark.conf.set("spark.sql.session.timeZone", "UTC")

craigslist_schema = types.StructType([
    types.StructField('posted',types.TimestampType()),
    types.StructField('region',types.StringType()),
    types.StructField('postingid',types.StringType()),
    types.StructField('image',types.StringType()),
    types.StructField('url',types.StringType()),
    types.StructField('labels',types.ArrayType(types.StringType())),
    types.StructField('beds',types.FloatType()),
    types.StructField('baths',types.FloatType()),
    types.StructField('city',types.StringType()),
    types.StructField('latitude',types.FloatType()),
    types.StructField('longitude',types.FloatType()),
    types.StructField('title', types.StringType()),
    types.StructField('price',types.FloatType()),
])

def transform(input_json):
    # labels - convert to lower and store as list
    label_arr=[]
    for key in input_json['labels']:
        label_arr.append(key.lower())
    input_json['labels']=label_arr

    # geo-coordinates
    coordinates = input_json['position'].split(';')
    input_json['latitude']=float(coordinates[0])
    input_json['longitude']=float(coordinates[1])
    del input_json['position']

    # price
    if(input_json['price']):
        price = input_json['price'][1:]
        input_json['price']=float(price)

    # convert all strings to lowercase
    for key in ['city', 'region']:
        input_json[key] = input_json[key].lower()
   
    # posting date
    post_time = datetime.datetime.strptime(input_json['posted'],"%Y-%m-%dT%H:%M:%S%z")
    input_json['posted']=post_time

    return input_json

def main(inputs):
    keyspace = "potatobytes"

    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect(keyspace)

    table = "craigslistcanada"
    session.execute("CREATE TABLE IF NOT EXISTS %s (posted TIMESTAMP,region TEXT,postingid TEXT PRIMARY KEY,image TEXT,url TEXT, labels LIST<TEXT>, beds FLOAT, baths FLOAT, city TEXT, latitude FLOAT, longitude FLOAT, title TEXT, price FLOAT);" %table)

    json_listings = inputs.map(json.loads)
    listings = json_listings.map(transform)

    listings = spark.createDataFrame(listings,schema=craigslist_schema)
    listings.write.format("org.apache.spark.sql.cassandra").options(table=table, keyspace=keyspace).save()

    # create table to store all posts favorited by user
    fav_table = "favorites"
    session.execute("CREATE TABLE IF NOT EXISTS %s (userid TEXT, postingid TEXT, PRIMARY KEY(userid, postingid));" %fav_table)
       
if __name__ == '__main__':
    inputs = sys.argv[1]
    text_input = sc.textFile(inputs)
    main(text_input)
