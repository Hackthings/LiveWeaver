from pycorenlp import StanfordCoreNLP
import nltk
from nltk.tree import ParentedTree

ROOT = 'ROOT'
if __name__ == '__main__':

    def addSentence(sentence):
        output = nlp.annotate(sentence, properties={
            'annotators': 'parse',
            'outputFormat': 'json'
        })

        assignPhrases(ParentedTree.fromstring(output['sentences'][0]['parse']))

    def assignPhrases(t):
        try:
            t.label()
        except AttributeError:
            return
        else:
            if t.label() in phraseTags:
                s = str(t.flatten())[1:-1]
                tag = str(s).split(' ')[0]
                phrase = ' '.join(str(s).split(' ')[1:])
                phraseInfo = {'tag': tag, 'phrase': phrase}
                ##send this to database
            if t.height() == 2:   #child nodes
                return

            for child in t:
                assignPhrases(child)


    
    
    nlp = StanfordCoreNLP('http://10.4.100.141:9000')

    phraseTags = ['ADJP','ADVP', 'CONJP', 'FRAG', 'INTJ', 'LST', 'NAC', 'NP', 'NX', 'PP', 'PRN','PRT','QP',
        'RRC','UCP','VP','WHADJP','WHAVP','WHNP','WHPP','X']
    #get sentence file as list of sentences
    #test data assigned for now
    sentences = ['This is my car.', 'Tom applied for the job.', 'Tom went back to his hometown.', 'I got a new camera.']

    for sentence in sentences:
        addSentence(sentence)
    
    