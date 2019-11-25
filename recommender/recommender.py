from pyspark.sql import SparkSession,functions,types
from pyspark.ml import Pipeline
from pyspark.sql.functions import udf
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
import sys


cluster_seeds=['127.0.0.1']
spark = SparkSession.builder.appName('Recommender').config('spark.cassandra.connection.host', ','.join(cluster_seeds)).getOrCreate()
assert spark.version>='2.4'
spark.sparkContext.setLogLevel('WARN')
sc = spark.sparkContext
spark.conf.set('spark.sql.session.timezone','UTC')


def main(city,keyspace,table):
    listings = spark.read.format('org.apache.spark.sql.cassandra').options(table=table,keyspace=keyspace).load()    
    #get all listings with same city name(includes all cases - upper, lower, capitalized)
    city_upper = city.upper() 
    city_caps = city.capitalize()
    city_list = listings.where((listings['city']==city) | (listings['city']==city_upper) | (listings['city']==city_caps))
    
    #find clusters
    train,validation = city_list.randomSplit([0.75,0.25])
    rec_assembler =  VectorAssembler(inputCols = ['beds','baths','latitude','longitude','price'], outputCol = 'features', handleInvalid='skip')
    kmeans = KMeans(k=6,seed=1)
    rec_pipeline = Pipeline(stages=[rec_assembler,kmeans])
    rec_model = rec_pipeline.fit(city_list)
    prediction = rec_model.transform(city_list)  #this dataframe contains clusters under the column prediction
    evaluator = ClusteringEvaluator()
    
    #score
    silhouette = evaluator.evaluate(prediction)
    print('Silhoutte score(k=6) with Euclidean distance '+str(silhouette))
   
    #compute centers in clusters
    centers = rec_model.stages[1].clusterCenters()
    print(centers)
    dist = udf(lambda features, prediction: features - centers[prediction])
    data = prediction.withColumn('distance', dist(prediction['features'], prediction['prediction']))
    data.createOrReplaceTempView('result')
    result = spark.sql('SELECT r.postingid,r.prediction,r.beds,r.baths,r.latitude,r.longitude,r.price,r.url FROM result as r')
    result.sort(result['prediction']).write.csv('vancouver_k6',mode='overwrite')

    """
    Modify commented part below for recommendations.
    
    query1 is the dataframe of favorited data. Right now works only for 1 favorite listing. Need to make changes to include multiple favorites.
    
    Suppose user has selected 4 favorites, out of the 4, 3 belong to cluster-0 and 1 belongs to cluster-1, give recommendations from cluster-0.
    query2 is the dataframe which contains all listings which belong to the same cluster as the favorited option in query 1.
    """

    """
    MODIFY:
    query1 = spark.sql('SELECT postingid,beds,baths,price,latitude,longitude,url,prediction,distance FROM result WHERE postingid=7014841049')
    query1.createOrReplaceTempView('query1')
    query1.show()

    query2= spark.sql('SELECT r.postingid,r.beds,r.baths,r.price,r.latitude,r.longitude,r.url,r.prediction FROM result as r,query1 as q WHERE q.prediction=r.prediction')
    query2.write.csv('query2',mode='overwrite')
    query2.show()
    """

if __name__ == '__main__':
    city = sys.argv[1]
    keyspace='potatobytes'
    table='recommender'
    main(city,keyspace,table)
