import sys,json
import re,string
from pyspark.sql import SparkSession,functions,types

#cluster_seeds = ['199.60.17.32']
cluster_seeds = ['127.0.0.1']       #faced an error here - possible fix necessary
spark = SparkSession.builder.appName('Spark Cassandra example').config('spark.cassandra.connection.host', ','.join(cluster_seeds)).getOrCreate()
assert spark.version>='2.4'
spark.sparkContext.setLogLevel('WARN')
spark.conf.set("spark.sql.session.timeZone", "GMT")

data = [
    ['ca-5682', 0],
    ['ca-nu', 0],
    ['ca-yt', 0],
    ['ca-nt', 0],
    ['ca-ab', 0],
    ['ca-nl', 0],
    ['ca-sk', 0],
    ['ca-mb', 0],
    ['ca-qc', 0],
    ['ca-on', 0],
    ['ca-nb', 0],
    ['ca-ns', 0],
    ['ca-pe', 0],
    ['ca-bc', 0]
]

class ChartData:
    def data1(self):
        df = spark.read.format("org.apache.spark.sql.cassandra") \
           .options(table='craigslistcanada', keyspace='potatobytes').load() 
        df.createOrReplaceTempView('df')

        output = spark.sql("SELECT LOWER(region) as region, count(*) as posts FROM df GROUP BY region ORDER BY posts").rdd.collect()
    
        for rows in output: 
            if (rows[0]=='ca-yk'):
                  data[2][1] = rows[1]
           
            for i in range(2,14):
                if(rows[0]==data[i][0]):
                    data[i][1]=rows[1]
        resp = data
        return resp

    def data2(self):
        resp = [
            ['ca-5682', 0],
            ['ca-bc', 1],
            ['ca-nu', 2],
            ['ca-nt', 3],
            ['ca-ab', 4],
            ['ca-nl', 5],
            ['ca-sk', 6],
            ['ca-mb', 7],
            ['ca-qc', 8],
            ['ca-on', 9],
            ['ca-nb', 10],
            ['ca-ns', 11],
            ['ca-pe', 12],
            ['ca-yt', 13]
        ]
        return resp
