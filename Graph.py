from pycorenlp import StanfordCoreNLP
import networkx as nx
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
    g.add_edges_from(conns)
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
        print(minIndex)
        for y in nnIndex:
            if(y!=minIndex):
                associations.append([x,minIndex,y,'1'])
        flag=1
        for y in output['sentences'][i]['basicDependencies']:
            if(y['dep']=='neg'):
                flag=-1
            if(y['dep'].endswith('mod')):
                associations.append([x,minIndex,y['dependent'],str(flag)])
        print(associations)

            

