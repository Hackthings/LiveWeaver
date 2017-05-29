from pycorenlp import StanfordCoreNLP
from nltk.tree import ParentedTree
import json
from watson_developer_cloud import AlchemyLanguageV1

INDEX = 0
ROOT = 'ROOT'
if __name__ == '__main__':

    class Coreference(object):
        coref_list = []
        def __init__(self, coref):
            self.coref_list.append(int(coref['sentNum'])-1)
            self.coref_list.append(int(coref['headIndex'])-1)
            self.coref_list.append(int(coref['startIndex'])-1)
            self.coref_list.append(int(coref['endIndex'])-1)

    class TokenResponse(object):
        def __init__(self, token):
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

    class emotions():
        def __init__(self, emotion_resp):
            self._anger = emotion_resp['docEmotions']['anger']
            self._disgust = emotion_resp['docEmotions']['disgust']
            self._fear = emotion_resp['docEmotions']['fear']
            self._joy = emotion_resp['docEmotions']['joy']
            self._sadness = emotion_resp['docEmotions']['sadness']

    class CustomTree(ParentedTree):
        corefs=[]
        def setToken(self, response):
            self.token = TokenResponse(response)

        def getToken(self):
            return self.token

        def setCoref(self, coref):
            self.corefs.append(Coreference(coref))

        def getCoref(self):
            return self.corefs

        def setEmotion(self, emotion_resp):
            self.emotion_analysis = emotions(emotion_resp)

    def assignTokens(t, output):
        try:
            t.label()
        except AttributeError:
            return
        else:
            if t.label() =='S':
                s = t.flatten()
                s = s[1:-1]
                alchemy_language = AlchemyLanguageV1(api_key = '15ce4bd07b66f9e000a15383777870c0afb383fb')
                emotion_resp = alchemy_language.emotion(text = s)
                t.setEmotion(emotion_resp)

            if t.height() == 2:   #child nodes
                global INDEX
                t.setToken(output['tokens'][INDEX])
                INDEX += 1
                return

            for child in t:
                assignTokens(child, output)

    def assign_corefs(t, output): #assign corefs only to those whose representative mention is false
        for i in output['corefs']:
            for x in output['corefs'][i]:
                if x['isRepresentativeMention'] == True:
                    y = x  #coref to be stored
            for x in output['corefs'][i]:
                if x != y:
                    trees[int(x['sentNum'])-1][int(x['headIndex'])-1][int(x['startIndex'])-1].setCoref(y)
    
    nlp = StanfordCoreNLP('http://10.4.100.141:9000')
    text = (
        'Pusheen and Smitha walked along the beach. Pusheen wanted to surf,'
        'but fell off the surfboard. Then they both laughed.')
    output = nlp.annotate(text, properties={
        'annotators': 'tokenize,ssplit,pos,depparse,parse,coref',
        'outputFormat': 'json'
    })
    #print(output['sentences'][0]['parse'])
    trees = []
    #traversing through all sentences

    for sentence in output['sentences']:
        trees.append(CustomTree.fromstring(sentence['parse'])) #array of trees
        INDEX = 0 #to keep count of word number inside sentence
        assignTokens(trees[sentence['index']], sentence)
    trees[0].draw()