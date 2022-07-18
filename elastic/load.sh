#!/bin/bash
python3 csv_to_es_json.py
docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .
curl --cacert http_ca.crt -u elastic:elastic -X PUT "https://localhost:9200/mir?pretty" -H 'Content-Type: application/json' -d'
    {
        "settings": {
            "index": {
            "number_of_shards": 1,  
            "number_of_replicas": 1 
            }
        },
        "mappings": {
            "properties": {
                "Tweet Id": { "type": "long" },
                "Text": { "type": "text" }
            }
        }
    }
    '
curl --cacert http_ca.crt -u elastic:elastic -H 'Content-Type: application/json' -XPOST 'https://localhost:9200/_bulk?pretty' --data-binary @./es_data.json
