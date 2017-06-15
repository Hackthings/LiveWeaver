from pycorenlp import StanfordCoreNLP
from scipy import spatial
nlp=StanfordCoreNLP('http://10.4.100.141:9000')
text='Timmy the elephant has eyes, ears, tusks and legs. Timmy the dog has four legs and four eyes. Timmy the hippo has a big nose and huge ears'
output = nlp.annotate(text, properties={'annotators': 'tokenize,ssplit,pos,depparse,parse,openie,ner','outputFormat': 'json'})
contexts=[]
words=[]
occsCont={}
for i in range(len(output['sentences'])):
    occs={}
    contexts.append(output['sentences'][i]['openie'][0]['subject'])
    for x in output['sentences'][i]['tokens']:
        if(x['pos']=='CD'or x['pos']=='JJ' or x['pos']=='NN' or x['pos']=='NNS'):
            words.append(x['word'])  
sWords=set(words)
for i in range(len(output['sentences'])):
    for x in sWords:
        occs[x]=0
        occsCont[i]=dict(occs)
for i in range(len(output['sentences'])):
    senWords=(text.split('.'))
    for x in sWords:
        occsCont[i][x]=senWords[i].count(x)
def getWord(id1,id2):
    pairs=c.execute('SELECT morph,wID FROM morphemes WHERE sID={v1}'.format(v1=id1,v2=id2))
    for x,y in pairs:  
        if(y==id2):
            return(x)
sim={}
for x in (range(1,len(contexts)+1)):
    simSmall={}
    sim[x]=dict(simSmall)
    for y in (range(1,len(contexts)+1)):
        sim[x][y]=1-spatial.distance.cosine(list(occsCont[x-1].values()),list(occsCont[y-1].values()))
print(sim)
