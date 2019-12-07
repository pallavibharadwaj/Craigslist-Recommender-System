#!/bin/sh

apt-get update

# to install scrapy on Ubuntu (or Ubuntu-based) systems, you need to install these dependencies:
apt-get install -y python3-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev libxslt-dev libxml2-dev

# install java openjdk
apt-get -y install openjdk-8-jdk --fix-missing

# install all required python packages
pip3 install -r requirements.txt

# installing spark-2.4.4
wget http://apache.mirror.colo-serv.net/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz
tar -xvzf spark-2.4.4-bin-hadoop2.7.tgz

# spark environment varibles
export SPARK_HOME='spark-2.4.4-bin-hadoop2.7/'
export PYSPARK_PYTHON='python3'
export PATH="$PATH:$SPARK_HOME/bin"

# Installing Cassandra Database
apt-get install cassandra -y --fix-missing

# start Cassandra automatically when the system boots:
systemctl enable cassandra

# spark-cassandra-connector:
git clone https://github.com/datastax/spark-cassandra-connector.git
cd spark-cassandra-connector/ && sbt/sbt assembly -Dscala-2.11=true
cp spark-cassandra-connector/spark-cassandra-connector/target/full/scala-2.11/spark-cassandra-connector-assembly-2.4.2-3-gda707460.jar $SPARK_HOME/jars/
