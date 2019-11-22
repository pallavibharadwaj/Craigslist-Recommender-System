import sys,json
import re,string
import datetime
from pyspark.sql import SparkSession,functions,types


#cluster_seeds = ['199.60.17.32']
cluster_seeds = ['127.0.0.1']       #faced an error here - possible fix necessary
spark = SparkSession.builder.appName('Spark Cassandra example').config('spark.cassandra.connection.host', ','.join(cluster_seeds)).getOrCreate()
assert spark.version>='2.4'
spark.sparkContext.setLogLevel('WARN')
sc = spark.sparkContext
spark.conf.set("spark.sql.session.timeZone", "GMT")

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
    types.StructField('position',types.ArrayType(types.FloatType())),
    types.StructField('title', types.StringType()),
    types.StructField('price',types.StringType()),
])  

def json_str(input_json):
    label_arr=[]
    geocodes = []
    for key in input_json['labels']:
        label_arr.append(key)
    coordinates = input_json['position'].split(';')
    for coordinate in coordinates:
        geocodes.append(float(coordinate))
    date_proper = datetime.datetime.strptime(input_json['posted'],"%Y-%m-%dT%H:%M:%S%z")
    input_json['labels']=label_arr
    input_json['position']=geocodes
    input_json['posted']=date_proper
    return input_json

def main(inputs):  
    json_listings = inputs.map(json.loads)
    listings = json_listings.map(json_str)
   
    listings_df = spark.createDataFrame(listings,schema=craigslist_schema)

    table="craigslistcanada" #table in cluster
    keyspace="potatobytes"    #keyspace created in cluster
    listings_df.write.format("org.apache.spark.sql.cassandra").options(table=table, keyspace=keyspace).save()
       
if __name__ == '__main__':
    inputs = sys.argv[1]
    text_input = sc.textFile(inputs)
    main(text_input)
