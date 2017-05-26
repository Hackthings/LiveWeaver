from pycorenlp import StanfordCoreNLP
from nltk.tree import ParentedTree

INDEX = 0
ROOT = 'ROOT'
from pycorenlp import StanfordCoreNLP
import nltk
from nltk.tree import Tree
from nltk.tree import ParentedTree
if __name__ == '__main__':
    nlp = StanfordCoreNLP('http://10.4.100.141:9000')
    text = (
        'Pusheen and Smitha walked along the beach. Pusheen wanted to surf,'
        'but fell off the surfboard. Then they both laughed.')
    output = nlp.annotate(text, properties={
        'annotators': 'tokenize,ssplit,pos,depparse,parse,coref',
        'outputFormat': 'json'
    })
    #print(output['sentences'][0]['parse'])
   
    print(output['corefs'])
   

    class Coreference(object):
            coref_list =[]
            def __init__(self,coref):
                
                coref_list.append(int(coref['sentNum'])-1)
                coref_list.append(int(coref['headIndex'])-1)
                coref_list.append(int(coref['startIndex'])-1)
                coref_list.append(int(coref['endIndex'])-1)
                                                         
     class TokenResponse(object):
        def __init__(self,token):
            self.index = token['index']
            self.word = token['word']
            self.original_text = token['originalText']
            self.lemma = token['lemma']
            self.characterOffsetBegin = token['characterOffsetBegin']
            self.characterOffsetEnd = token['characterOffsetEnd']
            self.pos = token['pos']
            self.ner = token['ner']    #FOR TASK 4 : NAMED ENTITY RECOGNITION
            self.speaker = token['speaker']
            self.before = token['before']
            self.after = token['after']
    
    
                

    class CustomTree(ParentedTree):
        corefs=[]
        def setToken(self,response):
            self.token = TokenResponse(response)

        def getToken(self):
            return self.token
        
        def setCoref(self,coref):
            self.corefs.append(Coreference(coref))

        def getCoref(self):
            return self.corefs
        
        
        
           
        
    def assignTokens(t, output):
        try:
            t.label()
        except AttributeError:
            return
        else:
                
            if t.height() == 2:   #chisld nodes
                #print(t)
                global INDEX
                t.setToken(output['tokens'][INDEX])
                INDEX += 1
                return

            for child in t:
                assignTokens(child, output)
    trees = []
#traversing through all sentences

    for sentence in output['sentences']:
        
        trees.append(CustomTree.fromstring(sentence['parse'])) #array of trees
        INDEX = 0 #to keep count of word number inside sentence
        assignTokens(trees[sentence['index']], sentence)
    trees[0].draw()
    
   #for i in output['corefs']:
        #for x in output['corefs'][i]:
             #print(trees[int(x['sentNum'])-1][int(x['headIndex'])-1][int(x['startIndex'])-1])
             #print(int(x['endIndex'])-1)
    # check for accessing corefs"""

            
    def assign_corefs(t,output):  # assign corefs only to those whose representative mention is false
        for i in output['corefs']:
            for x in output['corefs'][i]:
                if x['isRepresentativeMention'] == True:
                    y = x  #coref to be stored
            for x in output['corefs'][i]:
                if x != y:
                    trees[int(x['sentNum'])-1][int(x['headIndex'])-1][int(x['startIndex'])-1].setCoref(y)
                
