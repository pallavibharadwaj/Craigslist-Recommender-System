import sys,json
import re,string
from pyspark.sql import SparkSession,functions,types
from pyspark.sql.functions import lower

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

data2 = [
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
    def getpostcount(self):
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

    def median_rent(self):
        input_df = spark.read.format("org.apache.spark.sql.cassandra") \
            .options(table='craigslistcanada', keyspace='potatobytes').load()
        df0 = input_df.filter(input_df.beds.isNotNull())
        df = df0.withColumn('city',lower(input_df['city']))
        df.createOrReplaceTempView('df')

        cities = ['calgary','edmonton','montreal','ottawa','toronto','vancouver','waterloo']
        city_df = df.filter(df['city'].isin(cities))
        city_df.createOrReplaceTempView('city_df')
        output = spark.sql("SELECT lower(city) AS city,beds,count(*),approx_percentile(price,0.5) FROM city_df GROUP BY city,beds ORDER BY city").rdd.collect()
        resp = {}
        rent1=[]
        rent2=[]
        rent3=[]
        for row in output:
            if row[1]==1:
                rent1.append(row[3])
            if row[1]==2:
                rent2.append(row[3])
            if row[1]==3:
                rent3.append(row[3])
        resp['cities']=cities
        resp['rent1']=rent1
        resp['rent2']=rent2
        resp['rent3']=rent3
        return resp

    def pet_animals(self):        
        inputs = spark.read.format("org.apache.spark.sql.cassandra") \
            .options(table='craigslistcanada', keyspace='potatobytes').load()
        l = inputs.select(inputs['labels'])
        rows = l.rdd.collect()
        cats=0
        dogs=0
        both=0
        none=0
        total=0
        for row in rows:
            total=total+1
            if 'cats are OK - purrr' in row[0] and 'dogs are OK - wooof' in row[0]:
                both=both+1
            elif 'cats are OK - purrr' in row[0]:
                cats=cats+1
            elif 'dogs are OK - wooof' in row[0]:
                dogs=dogs+1
            else:
                none=none+1
        resp={'cats':cats,'dogs':dogs,'both':both,'none':none}
        for key in resp:
            resp[key]=round((resp[key]/total)*100,2)
        return resp


    def wheelchair(self):
        inputs = spark.read.format("org.apache.spark.sql.cassandra") \
        .options(table='craigslistcanada', keyspace='potatobytes').load()
        l = inputs.select(inputs['labels'])
        rows = l.rdd.collect()
        wheelchair=0
        none=0
        total=0
        for row in rows:
       	    total=total+1
            if 'wheelchair accessible' in row[0]:
                wheelchair=wheelchair+1
            else:
                none=none+1
        resp={'wheelchair':wheelchair,'none':none}
        for key in resp:
            resp[key]=round((resp[key]/total)*100,2)
        return resp

    def getaverageprice(self):
        df = spark.read.format("org.apache.spark.sql.cassandra") \
           .options(table='craigslistcanada', keyspace='potatobytes').load()
        df.createOrReplaceTempView('df')

        output = spark.sql("SELECT LOWER(region) as region, approx_percentile(price,0.5) as median_price FROM df GROUP BY region").rdd.collect()

        for rows in output:
            if (rows[0]=='ca-yk'):
                  data2[2][1] = rows[1]

            for i in range(2,14):
                if(rows[0]==data2[i][0]):
                    data2[i][1]=rows[1]
        resp = data2
        return resp
