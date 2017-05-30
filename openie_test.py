from pycorenlp import StanfordCoreNLP
import json
    
if __name__ == '__main__':  
    
    
    nlp = StanfordCoreNLP('http://10.4.100.141:9000')
    text = (
        'I will be a dancer')
    output = nlp.annotate(text, properties={
        'annotators': 'openie',
        'outputFormat': 'json'
    })

    print(output['sentences'][0]['openie'])
