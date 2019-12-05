import sys,json
import re,string
from pyspark.sql import SparkSession,functions,types
from pyspark.sql.functions import lower

#cluster_seeds = ['199.60.17.32']
cluster_seeds = ['127.0.0.1']       #faced an error here - possible fix necessary
spark = SparkSession.builder.appName('Spark Cassandra example').config('spark.cassandra.connection.host', ','.join(cluster_seeds)).getOrCreate()
assert spark.version>='2.4'
spark.sparkContext.setLogLevel('WARN')
spark.conf.set("spark.sql.session.timeZone", "UTC")
df = spark.read.format("org.apache.spark.sql.cassandra") \
           .options(table='craigslistcanada', keyspace='potatobytes').load().cache()
total_count = df.count()  #number of total records
df.createOrReplaceTempView('df')

 
class ChartData:
    def getpostcount(self):
        output = spark.sql("SELECT region, count(*) as posts FROM df GROUP BY region ORDER BY posts")
        default_df = spark.createDataFrame([['ca-5682', 0],['ca-nu', 0],['ca-yt', 0],['ca-nt', 0],['ca-ab', 0],['ca-nl', 0],['ca-sk', 0],['ca-mb', 0],['ca-qc', 0],['ca-on', 0],['ca-nb', 0],['ca-ns', 0],['ca-pe', 0],['ca-bc', 0]],['Region','Posts'])
        new_df = default_df.union(output)
        new_df = new_df.withColumn('region',functions.regexp_replace('region','ca-yk','ca-yt'))
        data = new_df.groupBy('region').sum().collect()
        return data    

    def median_rent(self):
        filtered_df = df.filter(df.beds.isNotNull())

        cities = ['calgary','edmonton','montreal','ottawa','toronto','vancouver','waterloo']
        city_df = df.filter(df['city'].isin(cities))
        city_df.createOrReplaceTempView('city_df')
        output = spark.sql("SELECT city,beds,count(*),approx_percentile(price,0.5) FROM city_df GROUP BY city,beds ORDER BY city").rdd.collect()
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
        cats = df.filter(functions.array_contains(df['labels'],'cats are ok - purrr'))
        both  = cats.filter(functions.array_contains(cats['labels'],'dogs are ok - wooof'))
        both_count = both.count()

        dogs = df.filter(functions.array_contains(df['labels'],'dogs are ok - wooof'))
        dog_count = dogs.count() - both_count
        cat_count = cats.count() - both_count
        none = total_count - (cat_count+dog_count+both_count)
        resp={'cats':cat_count,'dogs':dog_count,'both':both_count,'none':none}
        for key in resp:
            resp[key]=round((resp[key]/total_count)*100,2)
        return resp

    def wheelchair(self):
        wheelchair = df.filter(functions.array_contains(df['labels'],'wheelchair accessible'))
        wheelchair_count = wheelchair.count()
        resp={'wheelchair':wheelchair_count,'none':total_count-wheelchair_count}
        for key in resp:
            resp[key]=round((resp[key]/total_count)*100,2)
        return resp

    def getaverageprice(self):
        output = spark.sql("SELECT region, approx_percentile(price,0.5) as median_price FROM df GROUP BY region")
        default_df = spark.createDataFrame([['ca-5682', 0],['ca-nu', 0],['ca-yt', 0],['ca-nt', 0],['ca-ab', 0],['ca-nl', 0],['ca-sk', 0],['ca-mb', 0],['ca-qc', 0],['ca-on', 0],['ca-nb', 0],['ca-ns', 0],['ca-pe', 0],['ca-bc', 0]],['Region','Posts'])
        new_df = default_df.union(output)
        new_df = new_df.withColumn('region',functions.regexp_replace('region','ca-yk','ca-yt'))
        data = new_df.groupBy('region').sum().collect()
        return data

    def getboxplotvalues(self):
        new_df = df.filter(df.price<=5000).filter(df.price>0)
        new_df.createOrReplaceTempView('new_df')

        output = spark.sql("SELECT region, min(price) as min, approx_percentile(price,0.25) as q1, approx_percentile(price,0.5) as median_price, approx_percentile(price,0.75) as q3, max(price) as max FROM new_df GROUP BY region ORDER BY region").rdd.collect()
        resp = {}
        regions = []
        val = []
        for rows in output:
            regions.append(rows[0])
            val.append([rows[1],rows[2],rows[3],rows[4],rows[5]])
        resp['regions'] = regions
        resp['val'] = val
        return resp

    def getsplinevalues(self):
        values = spark.sql("SELECT Region, DAYOFWEEK(posted) as DAY, count(*) as count from df GROUP BY day,region ORDER BY region,DAY").rdd.collect()
        default = [['ca-yk', [0,0,0,0,0,0,0]],['ca-nt', [0,0,0,0,0,0,0]],['ca-ab', [0,0,0,0,0,0,0]],['ca-nl', [0,0,0,0,0,0,0]],['ca-sk', [0,0,0,0,0,0,0]],['ca-mb', [0,0,0,0,0,0,0]],['ca-qc', [0,0,0,0,0,0,0]],['ca-on', [0,0,0,0,0,0,0]],['ca-nb', [0,0,0,0,0,0,0]],['ca-ns', [0,0,0,0,0,0,0]],['ca-pe', [0,0,0,0,0,0,0]],['ca-bc', [0,0,0,0,0,0,0]]]
        for val in values :
            for entry in default :
                if (entry[0]==val['Region']):
                    entry[1][val[1]-1]=val[2]
        return default
