from pycorenlp import StanfordCoreNLP
import networkx as nx
import sqlite3
nlp = StanfordCoreNLP('http://10.4.100.141:9000')
text = input()
output = nlp.annotate(text, properties={'annotators': 'tokenize,ssplit,pos,depparse,parse,lemma','outputFormat': 'json'})
def bfs_paths(graph, start, goal):
    # keep track of explored nodes
    explored = []
    # keep track of all the paths to be checked
    queue = [[start]]
 
    # return path if start is goal
    if start == goal:
        return "That was easy! Start = goal"
 
    # keeps looping until all possible paths have been checked
    while queue:
        # pop the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        if node not in explored:
            neighbours = graph[node]
            # go through all neighbour nodes, construct a new path and
            # push it into the queue
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                # return path if neighbour is goal
                if neighbour == goal:
                    return new_path
 
            # mark node as explored
            explored.append(node)
conn=sqlite3.connect('Morphemes.sqlite')
c=conn.cursor()
c.execute('CREATE TABLE morphemes (morph TEXT, sID INTEGER, wID INTEGER)')
for i in range(len(output['sentences'])):
    for x in output['sentences'][i]['tokens']:
        c.execute('INSERT INTO morphemes(morph,sID,wID) VALUES(?,?,?)',(x['lemma'],i+1,x['index']))
    inheritances=[]
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
    g.add_edges_from(conns)
    for x in nnpIndex:
        paths=[]
        wordDist=[]
        minIndex=0
        for y in nnIndex:
            paths.append(list(bfs_paths(g,x,y)))
            wordDist.append(abs(x-y))
        if(len(paths)==1):
            if(len(paths[0])==2 or paths[0]==3):
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
        flag=1
        inNeg=0
        for t in range(minIndex):
            if(output['sentences'][i]['basicDependencies'][t]['dep']=='neg'):
                flag=-1
                inNeg=t+1
        inheritances.append([i+1,x,minIndex,flag])
        print([i+1,x,minIndex,flag])
        for y in nnIndex:
            if(y!=minIndex and minIndex!=0):
                associations.append([i+1,x,minIndex,y,1])
        flag=1
        for y in output['sentences'][i]['basicDependencies']:
            if(y['dep']=='neg' and y['dependent']!=inNeg):
                flag=-1
            if(y['dep'].endswith('mod') and y['dep']!='nmod'):
                if(minIndex!=0):
                    associations.append([i+1,x,minIndex,y['dependent'],flag])
                associations.append([i+1,x,y['dependent'],y['governor'],1])
        print(associations)
def getWord(id1,id2):
    pairs=c.execute('SELECT morph,wID FROM morphemes WHERE sID={v1}'.format(v1=id1,v2=id2))
    for x,y in pairs:
        if(y==id2):
            return(x)
for x in inheritances:
    print(x[0],getWord(x[0],x[1]),getWord(x[0],x[2]),x[3])
for x in associations:
    print(x[0],getWord(x[0],x[1]),getWord(x[0],x[2]),getWord(x[0],x[3]),x[4])
            
