from pycorenlp import StanfordCoreNLP
import json
    
if __name__ == '__main__':  
    
    
    nlp = StanfordCoreNLP('http://10.4.100.141:9000')
    text = (
        "I'm done")
    output = nlp.annotate(text, properties={
        'annotators': 'tokenize,ssplit,pos,depparse,parse,openie',
        'outputFormat': 'json'
    })

    print(json.dumps(output['sentences'], indent = 4))
