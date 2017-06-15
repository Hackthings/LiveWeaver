from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://10.4.100.141:9000')
text = input()
output = nlp.annotate(text, properties={
        'annotators': 'tokenize,ssplit,pos,depparse,parse,lemma',
        'outputFormat': 'json'
    })
morphs = []
for i in range(len(output['sentences'])):
    for x in output['sentences'][i]['tokens']:
        if(x['lemma'].isalnum()):
            morphs.append(x['lemma'])
print(morphs)