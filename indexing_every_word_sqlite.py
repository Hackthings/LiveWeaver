from pycorenlp import StanfordCoreNLP
import nltk
from nltk.tree import ParentedTree
import sqlite3
ROOT = 'ROOT'
if __name__ == '__main__':

    phraseTags = ['ADJP', 'ADVP', 'CONJP', 'FRAG', 'INTJ', 'LST', 'NAC', 'NP', 'NX', 'PP', 'PRN', 'PRT', 'QP',
                  'RRC', 'UCP', 'VP', 'WHADJP', 'WHAVP', 'WHNP', 'WHPP', 'X']
    conn = sqlite3.connect("phrase_duplicate.db")

    conn.execute("CREATE TABLE WORD_INDEX(SEN_ID INT NOT NULL, PHRASE_ID INT NOT NULL, WORD_ID INT NOT NULL);")

    le = []
    def addSentence(sentence):
        output = nlp.annotate(sentence, properties={
            'annotators': 'parse',
            'outputFormat': 'json'
        })

        tr = ParentedTree.fromstring(output['sentences'][0]['parse'])
        le.append(tr.leaves())
        assignPhrases(tr)

    phraseInfo = []
    phrase_per_sent = []
    my_list = []
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
                phraseInfo.append({'tag': tag, 'phrase': phrase})
            if t.height() == 2:  # child nodes
                return

            for child in t:
                assignPhrases(child)

    nlp = StanfordCoreNLP('http://10.4.100.141:9000')

    # test data assigned for now
    sentences = ['This is my car', 'Tom has my car',
                 'Tom has a house', 'I got a new car']
    k = 0
    dict = {}
    flag = 0

    for i in range(len(sentences)):
        addSentence(sentences[i])
        phrase_per_sent.append(phraseInfo)
        phraseInfo = []
        for j in range(len(le[0])):
            if le[0][j] in dict:
                continue
            else:
                dict.update({le[0][j]:flag})
                flag = flag+1
        le = []
    for j in range(len(phrase_per_sent)):
        for i,p in enumerate(phrase_per_sent[j]):
            for n in range(len(p['phrase'].split())):
                wid = dict.get(p['phrase'].split()[n])
                my_list.append([j+1,i+1,wid+1])
    for item in my_list:
        conn.execute('insert into WORD_INDEX values (?,?,?)', (item[0],item[1],item[2]))
    cursor = conn.execute("SELECT * from WORD_INDEX")
    for row in cursor:
        print(row)






