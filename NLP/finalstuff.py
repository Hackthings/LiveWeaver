import elasticsearch
import wikipedia
import sqlite3

settings = \
    {
        "settings":
            {
                "index":
                    {
                        "analysis":
                            {
                                "analyzer":
                                    {
                                        "my_ngram_analyzer":
                                            {
                                                "tokenizer": "my_ngram_tokenizer",
                                                "filter": ["lowercase"]
                                            }
                                    },
                                "tokenizer":
                                    {
                                        "my_ngram_tokenizer":
                                            {
                                                "type": "nGram",
                                                "min_gram": "2",
                                                "max_gram": "5",
                                                "token_chars": ["letter", "digit"]
                                            }
                                    },
                            }

                    }
            },
        "mappings":
            {
                "parah":
                    {
                        "properties":
                            {
                                "parah":
                                    {
                                        "type": "string",
                                        "term_vector": "yes",
                                        "analyzer": "my_ngram_analyzer"
                                    }
                            }
                    }
            }
    }

def search_res(query):
    hits = es.search(index= 'paragraphs',body=query)
    result = [('()'.join([hit['_id'], hit['_type']]), hit['_score']) for hit in hits['hits']['hits']]
    if not result:
        return [("1()wiki", 1)]
    return result
    """except Exception as e:
        es.index(content={"content": query['query']['match']['content'], "body": settings},id=1)
        hits = es.search(index = namescope_as_index, doc_type = "doc", body = query,)
        result = [('()'.join([hit['_id'], hit['_type']]), hit['_score']) for hit in hits['hits']['hits']]
        if not result:
            return [("1()wiki", 1)]
        return result"""
conn = sqlite3.connect('test.db')
c = conn.cursor()
#c.execute('CREATE TABLE Articles1 (Primary_ID INTEGER PRIMARY KEY AUTOINCREMENT,Namescope_ID INT, Para_ID INT, Namescope TEXT, Title TEXT, Para_content TEXT, Cluster_ID INT);')
es = elasticsearch.Elasticsearch('10.4.100.32:9200')
namescopes = []
def getclID(article):
    res = search_res({"query": {"match": {"content": article}}})
    print(res)
    max = 0
    maxid = 0
    for resid in res:
        if (resid[1] > max and (int((resid[0].split('()'))[0])<row1[0])):
            max = resid[1]
            maxid = int((resid[0].split('()'))[0])
    return maxid
for i in range(2):
    try:
        namescopes.append(wikipedia.random())
        articles_names = wikipedia.search(namescopes[i], results=3)
        namescopes[i] = ("_".join(namescopes[i].split())).lower()
        articles = []
        articlesJSON = []
        clID = []
    except wikipedia.exceptions.DisambiguationError as e:
        print(e)
        i = i-1
        continue
    for x in range(3):
        try:
            articles.append(wikipedia.page(articles_names[x]))
            articlesJSON.append({"content": articles[x].summary})
            articles_names[x] = ("_".join(articles_names[x].split())).lower()

            c.execute('INSERT INTO Articles1(Namescope_ID, Para_ID, Namescope, Title, Para_content) VALUES(?,?,?,?,?)',
                      (i + 1, x + 1, namescopes[i], articles[x].title, articles[x].summary))

        except wikipedia.exceptions.DisambiguationError as e:
            print(e)
            x = x-1
            continue
cur = c.execute("SELECT Primary_ID, Namescope, Title, Para_content FROM Articles1")
for row in cur:
    es.index(index='paragraphs', doc_type=row[1] + ":" + row[2], id=row[0], body={'content': row[3]})
for o in range(1000):
    continue
cur1 = c.execute("SELECT Primary_ID, Namescope, Title, Para_content FROM Articles1")
for row1 in cur1:
    if (row1[0] == 1):
        clID.append(1)
    else:
        clID.append(getclID(row1[3]))
    print(clID)
    print(row1[0] + " " + row1[2])
#     c.execute("UPDATE Articles1 SET Cluster_ID = ? WHERE Primary_ID = ?", (clID[row1[0]-1], row1[0]))
# cur2 = c.execute("SELECT Cluster_ID, Namescope, Primary_ID FROM Articles1")
# for k in cur2:
#     print(k)

