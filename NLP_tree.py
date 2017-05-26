from pycorenlp import StanfordCoreNLP
from nltk.tree import ParentedTree

INDEX = 0
ROOT = 'ROOT'
class tokenInfo():
    def __init__(self, response, coref = 'null'):
        self._word = response['word']
        self._originalText = response['originalText']
        self._characterOffsetBegin = response['characterOffsetBegin']
        self._characterOffsetEnd = response['characterOffsetEnd']
        self._pos = response['pos']
        self._before = response['before']
        self._after = response['after']
        self._lemma = response['lemma']
        self._coref = coref

class customTree(ParentedTree):

    def setToken(self, tokenResponse):
        print("reached token response")
        self._token = tokenInfo(tokenResponse)

    def getToken(self):
        return self._token

def assignTokens(t, output):
    try:
        t.label()
    except AttributeError:
        return
    else:

        if t.height() == 2:   #child nodes
            print(t)
            global INDEX
            t.setToken(output['tokens'][INDEX])
            INDEX += 1
            return

        for child in t:
            assignTokens(child, output)

nlp = StanfordCoreNLP('http://10.4.100.141:9000')

text = (
    'Pusheen and Smitha walked along the beach. '
    'She wanted to surf, but fell off the surfboard.')

output = nlp.annotate(text, properties={
    'annotators': 'tokenize,ssplit,pos,depparse,parse,coref',
    'outputFormat': 'json'})

trees = []
#traversing through all sentences
for sentence in output['sentences']:
    print(type(sentence['index']))
    trees.append(customTree.fromstring(sentence['parse'])) #array of trees
    INDEX = 0 #to keep count of word number inside sentence
    assignTokens(trees[sentence['index']], sentence)

for i in output['corefs']:
    for x in output['corefs'][i]:
        print(x) #travesring through corefs, have to assign them

#random change to check git
#again
#just experimenting
