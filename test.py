from datetime import datetime 
from elasticsearch import Elasticsearch

es = Elasticsearch("192.168.1.157:9200")

data = {
    "timestamp" : datetime.now().strftime( "%Y-%m-%dT%H:%M:%S.000+0800" ),
    "http_code" :"404",
    "count" :"10"
}

es.index( index="http_code", doc_type="error_code", body=data )