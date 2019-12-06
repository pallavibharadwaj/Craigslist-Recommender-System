from cassandra.cluster import Cluster
from pyspark.sql import SparkSession, types
from pyspark.ml import Pipeline
from pyspark.sql.functions import udf, to_json, col, struct
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator


cluster = Cluster(['127.0.0.1'])
keyspace = "potatobytes"
session = cluster.connect(keyspace)

cluster_seeds=['127.0.0.1']
spark = SparkSession.builder.appName('Recommender').config('spark.cassandra.connection.host', ','.join(cluster_seeds)).getOrCreate()
assert spark.version>='2.4'
spark.sparkContext.setLogLevel('WARN')
sc = spark.sparkContext
spark.conf.set('spark.sql.session.timezone','UTC')

listings_table = 'craigslistcanada'
fav_table = 'favorites'

class ListingData:
    def getAllFavorites(self):
        resp = []
        try:
            listings = spark.read.format("org.apache.spark.sql.cassandra") \
               .options(table=listings_table, keyspace=keyspace).load()
            favorites = spark.read.format("org.apache.spark.sql.cassandra") \
                .options(table=fav_table, keyspace=keyspace).load()

            # get all user's favorites
            listings.createOrReplaceTempView('listings')
            favorites.createOrReplaceTempView('favorites')
            favorites = spark.sql("SELECT l.* from listings as l \
                        WHERE l.postingid IN (SELECT DISTINCT postingid FROM favorites WHERE userid='potato')")

            resp = favorites.rdd.collect()
        except:
            print("Error fetching all favorites")
        return resp

    def find_similar(self, predictions, favorites):
        similar = spark.range(0).drop("id")
        try:
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
        except:
            print("Error finding similar items")
        return similar

    def clusterize(self, data, kval):
        clusters = spark.range(0).drop("id")
        try:
            assembler =  VectorAssembler(inputCols = ['beds','baths','price'], outputCol = 'features', handleInvalid='skip')
            kmeans = KMeans(k=kval,seed=1)
            pipeline = Pipeline(stages=[assembler,kmeans])
            model = pipeline.fit(data)

            # returns all posts with cluster numbers assigned to each under column prediction
            clusters = model.transform(data)
        except:
            print("Error clusterizing inputs")

        return clusters

    def getAllSimilar(self):
        resp = []
        try:
            listings = spark.read.format('org.apache.spark.sql.cassandra').options(table=listings_table,keyspace=keyspace).load().cache()
            # read favorited listings
            favorites = spark.read.format('org.apache.spark.sql.cassandra').options(table=fav_table,keyspace=keyspace).load().cache()

            if(not favorites.rdd.isEmpty()):
                # one value at any given time
                city = spark.sql("SELECT city from listings as l \
                    WHERE l.postingid=(SELECT postingid FROM favorites WHERE userid='potato' LIMIT 1)").collect()[0]['city']
                # get all listings with in the city
                data = listings.where(listings['city']==city)

                kval = 15
                prediction = self.clusterize(data, kval)
                evaluator = ClusteringEvaluator()

                silhouette = evaluator.evaluate(prediction)    #score
                print('Silhoutte score(k=%s) with Euclidean distance : %s' % (kval, silhouette) )

                # find similar posts
                similar = self.find_similar(prediction, favorites)
                resp = similar.drop('features').rdd.collect()
        except:
            print("Error fetching similar items")

        return resp