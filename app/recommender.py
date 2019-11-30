from cassandra.cluster import Cluster
from pyspark.sql import SparkSession, types
from pyspark.ml import Pipeline
from pyspark.sql.functions import udf, to_json, col, struct
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator


#cluster_seeds = ['199.60.17.32']
cluster = Cluster(['127.0.0.1'])
keyspace = "potatobytes"
session = cluster.connect(keyspace)

cluster_seeds=['127.0.0.1']
spark = SparkSession.builder.appName('Recommender').config('spark.cassandra.connection.host', ','.join(cluster_seeds)).getOrCreate()
assert spark.version>='2.4'
spark.sparkContext.setLogLevel('WARN')
sc = spark.sparkContext
spark.conf.set('spark.sql.session.timezone','UTC')

class ListingData:
    def getAllFavorites(self):
        listings = spark.read.format("org.apache.spark.sql.cassandra") \
           .options(table='craigslistcanada', keyspace='potatobytes').load()
        favorites = spark.read.format("org.apache.spark.sql.cassandra") \
            .options(table='favorites', keyspace='potatobytes').load()

        # get all user's favorites
        listings.createOrReplaceTempView('listings')
        favorites.createOrReplaceTempView('favorites')
        favorites = spark.sql("SELECT l.* from listings as l \
                    WHERE l.postingid IN (SELECT DISTINCT postingid FROM favorites WHERE userid='potato')")

        resp = favorites.rdd.collect()
        return resp

    def find_similar(self, predictions, favorites):
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

    def clusterize(self, data, kval):
        assembler =  VectorAssembler(inputCols = ['beds','baths','price'], outputCol = 'features', handleInvalid='skip')
        kmeans = KMeans(k=kval,seed=1)
        pipeline = Pipeline(stages=[assembler,kmeans])
        model = pipeline.fit(data)

        # returns all posts with cluster numbers assigned to each under column prediction
        clusters = model.transform(data)

        return clusters

    def getAllSimilar(self):
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
        prediction = self.clusterize(data, kval)
        evaluator = ClusteringEvaluator()

        silhouette = evaluator.evaluate(prediction)    #score
        print('Silhoutte score(k=%s) with Euclidean distance : %s' % (kval, silhouette) )

        # find similar posts
        similar = self.find_similar(prediction, favorites)
        resp = similar.drop('features').rdd.collect()

        return resp