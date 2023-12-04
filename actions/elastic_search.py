from elasticsearch import Elasticsearch


def elastic_search(query):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    content = []
    body = {"query": {
        "match": {
            "content": {
                "query": query
            }
        }
    }
    }
    res = es.search(index="my_book_index", body=body)
    for document in res['hits']['hits']:
        content.append(document['_source']['content'])
    return content
