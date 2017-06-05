from pycorenlp import StanfordCoreNLP
import networkx as nx
nlp = StanfordCoreNLP('http://10.4.100.141:9000')
text = input()
output = nlp.annotate(text, properties={'annotators': 'tokenize,ssplit,pos,depparse,parse,lemma','outputFormat': 'json'})
print(output)

def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))

for i in range(len(output['sentences'])):
    associations=[]
    nnpIndex=[]
    nnIndex = []
    tpl = ()
    conns = []
    g = nx.Graph()
    for x in output['sentences'][i]['tokens']:
        if x['pos']=='NNP':
            nnpIndex.append(x['index'])
        if x['pos']=='NN' or x['pos']=='NNS':
            nnIndex.append(x['index'])
    for x in output['sentences'][i]['basicDependencies']:
        tpl = (x['governor'],x['dependent'])
        conns.append(tpl)
    for x in conns:
        g.add_edge(x[0],x[1])
    for x in nnpIndex:
        paths=[]
        wordDist=[]
        minIndex=0
        for y in nnIndex:
            paths.append(list(bfs_paths(g,x,y)))
            wordDist.append(abs(x-y))
        if(len(paths)==1):
            if(len(paths[0])==2):
                minIndex=nnIndex[0]
            else:
                minIndex=0
        else:
            minIndex=nnIndex[wordDist.index(min(wordDist))]
            minPath=len(paths[wordDist.index(min(wordDist))])
            for y in range(len(paths)):
                if(len(paths[y])<minPath):
                    minPath=len(paths[y])
                    minIndex=nnIndex[y]
        for y in nnIndex:
            if(y!=minIndex):
                associations.append([x,minIndex,y,'+1'])
        flag=1
        for y in output['sentences'][i]['basicDependencies']:
            if(y['dep']=='neg'):
                flag=-1
            if(y['dep'].endswith('mod')):
                associations.append([x,minIndex,y,str(flag)])


            