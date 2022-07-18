#!/bin/bash
docker network create elastic
docker run --name es01 --net elastic -e ES_JAVA_OPTS="-Xms2g -Xmx2g" -e ELASTIC_PASSWORD="elastic" -p 9200:9200 -p 9300:9300 -it docker.elastic.co/elasticsearch/elasticsearch:8.3.2
