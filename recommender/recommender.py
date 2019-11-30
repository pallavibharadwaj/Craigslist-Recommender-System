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

def find_similar(predictions, favorites):
    predictions.createOrReplaceTempView('predictions')
    favorites.createOrReplaceTempView('favorites')

    # cluster numbers of favorites -> all posts in the cluster
    similar = spark.sql("SELECT p.* from predictions as p \
                    WHERE prediction IN (SELECT DISTINCT p.prediction FROM predictions as p, favorites as f \
                            WHERE f.postingid = p.postingid)")

    # all posts in the cluster except the already favorited
    similar.createOrReplaceTempView('similar')
    similar = spark.sql("SELECT s.* FROM similar AS s \
                    WHERE s.postingid NOT IN (SELECT postingid FROM favorites)")
    return similar

def clusterize(data, kval):
    assembler =  VectorAssembler(inputCols = ['beds','baths','price'], outputCol = 'features', handleInvalid='skip')
    kmeans = KMeans(k=kval,seed=1)
    pipeline = Pipeline(stages=[assembler,kmeans])
    model = pipeline.fit(data)

    # returns all posts with cluster numbers assigned to each under column prediction
    clusters = model.transform(data)

    return clusters


def main():
    city = 'halifax'

    keyspace='potatobytes'
    listings_table = 'craigslistcanada'
    fav_table = 'favorites'
    listings = spark.read.format('org.apache.spark.sql.cassandra').options(table=listings_table,keyspace=keyspace).load()
    # read favorited listings
    favorites = spark.read.format('org.apache.spark.sql.cassandra').options(table=fav_table,keyspace=keyspace).load()

    # get all listings with same city name(includes all cases - upper, lower, capitalized)
    city_upper = city.upper() 
    city_caps = city.capitalize()
    data = listings.where((listings['city']==city) | (listings['city']==city_upper) | (listings['city']==city_caps))

    kval = 15   #TODO: find a way to initialize this value
    prediction = clusterize(data, kval)
    evaluator = ClusteringEvaluator()

    silhouette = evaluator.evaluate(prediction)    #score
    print('Silhoutte score(k=%s) with Euclidean distance : %s' % (kval, silhouette) )

    # find similar posts
    similar = find_similar(prediction, favorites)

    """
    #compute centers in clusters
    centers = rec_model.stages[1].clusterCenters()
    print(centers)
    dist = udf(lambda features, prediction: features - centers[prediction])
    data = prediction.withColumn('distance', dist(prediction['features'], prediction['prediction']))
    data.createOrReplaceTempView('result')
    result = spark.sql('SELECT r.postingid,r.prediction,r.beds,r.baths,r.latitude,r.longitude,r.price,r.url FROM result as r')
    result.sort(result['prediction']).write.csv('vancouver_k6',mode='overwrite')
    """

if __name__ == '__main__':
    main()
