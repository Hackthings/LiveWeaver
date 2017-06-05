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
								"analyzer" :
									{
										"my_ngram_analyzer":
											{
												"tokenizer": "my_ngram_tokenizer",
												"filter"   : ["lowercase"]
											}
									},
								"tokenizer":
									{
										"my_ngram_tokenizer":
											{
												"type"       : "nGram",
												"min_gram"   : "2",
												"max_gram"   : "5",
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
										"type"       : "string",
										"term_vector": "yes",
										"analyzer"   : "my_ngram_analyzer"
									}
							}
					}
			}
	}

class Indexer:

	def __init__(self, moniker, server):
		self.__index__  = els.Elasticsearch(server)
		self.__moniker__= moniker
	
	def index(self, content, id=None, provider=None ):
		if id and provider:
			return self.__index__.index\
			(
				index       = self.__moniker__,
				doc_type    = provider,
				body        = content,
				id          = id
			)
		if not id and provider:
			return self.__index__.index \
			(
				index = self.__moniker__,
				doc_type = provider,
				body = content,
			)
		if id and not provider:
			return self.__index__.index \
					(
					index = self.__moniker__,
					doc_type = "doc",
					body = content,
					id = id
				)
		if not id and not provider:
			return self.__index__.index\
			(
				index       = self.__moniker__,
				doc_type    = "doc",
				body        = content
			)
	def search(self, query, provider = None):
		try:
			if provider:
				hits = \
				self.__index__.search \
				(

					index       = self.__moniker__,
					doc_type    = provider,
					body        = query,

				)
				result = [('()'.join([hit['_id'], hit['_type']]), hit['_score']) for hit in hits['hits']['hits']]
				if not result:
					return [("1()wiki", 1)]
				return result
			else:
				hits = \
				self.__index__.search \
				(
					index   = self.__moniker__,
					doc_type = "doc",
					body    = query,
				)

				result = [('()'.join([hit['_id'], hit['_type']]), hit['_score']) for hit in hits['hits']['hits']]

				if not result:
					return [("1()wiki",1)]
				return result
		except Exception as e:
			self.index(provider = provider, content = {"content": query['query']['match']['content'], "body": settings}, id = 1)
			hits = \
				self.__index__.search \
						(

						index = self.__moniker__,
						doc_type = provider,
						body = query,

					)
			result = [('()'.join([hit['_id'], hit['_type']]), hit['_score']) for hit in hits['hits']['hits']]
			if not result:
				return [("1()wiki", 1)]
			return result
table_name='Articles'
field_1='Primary ID'
field_2='Title'
field_3='Paragraph'
field_4='Cluster ID'
field_1type='INTEGER'
field_2type='TEXT'
field_3type='TEXT'
field_4type='INTEGER'
conn=sqlite3.connect('test.sqlite')
c=conn.cursor()
c.execute('CREATE TABLE {tn} ({f1} {f1t},{f2} {f2t},{f3} {f3t},{f4} {f4t})'.format(tn=table_name, f1=field_1,f1t=field_1type,f2=field_1,f2t=field_2type,f3=field_3,f3t=field_3type,f4=field_4,f4t=field_4type))
es=elasticsearch.Elasticsearch('10.4.100.32:9200')
namescopes=[]
def getclID(article,title):
            res=es.search({"query": {"match": {"content": article}}},title)
            resid = []
            max=0
            maxid=0
            for resid in res:
                resid=resid.split('()')
                if resid[2]>max:
                    max=resid[2]
                    maxid = resid[0] 
            return maxid
for i in range(40):
    namescopes.append(wikipedia.random())
    articles_names=wikipedia.search(namescopes[i],results=10000)
    articles=[]
    articlesJSON=[] 
    clID=[]
	
    for x in range(10000):
        articles.append(wikipedia.page(articles_names[x]))
        articlesJSON.append({"content":articles[x].summary})#From here on out think of a way to index it after searching. I made a function get clID. Use it somehow.
        if(x==1):
            clID.append('1')
            es.index(index=namescopes[i], doc_type=articles_names[x], id=x, body=articlesJSON[x])
        else:
            clID.append(getclID(articlesJSON[x].summary,articles[x].title))
            es.index(index=namescopes[i], doc_type=articles_names[x], id=x, body=articlesJSON[x])
        try:
            c.execute('INSERT INTO {tn} ({f1},{f2},{f3},{f4}) VALUES(x1,x2,x3,x4)'.format(tn=table_name,f1=field_1,f2=fiel2,f3=field_3,f4=field_4,x1=x+1,x2=articles[x].title,x3=articles[x].summary,x4=clID[x])) 
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column {}'.format(field_1))
    
		