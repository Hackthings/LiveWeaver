from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://10.4.100.141:9000')
text = 'The dog who bit the toddler was named Benji.'
output = nlp.annotate(text, properties={
        'annotators': 'tokenize,ssplit,pos,depparse,parse,lemma',
        'outputFormat': 'json'
    })
print(output)
