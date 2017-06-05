from pycorenlp import StanfordCoreNLP
import nltk
from nltk.tree import ParentedTree
import sqlite3
ROOT = 'ROOT'
if __name__ == '__main__':

    phraseTags = ['ADJP', 'ADVP', 'CONJP', 'FRAG', 'INTJ', 'LST', 'NAC', 'NP', 'NX', 'PP', 'PRN', 'PRT', 'QP',
                  'RRC', 'UCP', 'VP', 'WHADJP', 'WHAVP', 'WHNP', 'WHPP', 'X']
    conn = sqlite3.connect("phrase_duplicate.db")

    conn.execute("CREATE TABLE PHRASE_DUPLICATION7 (ID INT NOT NULL, PHRASE_TYPE TEXT NOT NULL, PHRASE_TEXT_NUM TEXT NOT NULL, PHRASE_ID INT NOT NULL);")


    def addSentence(sentence):
        output = nlp.annotate(sentence, properties={
            'annotators': 'parse',
            'outputFormat': 'json'
        })



        assignPhrases(ParentedTree.fromstring(output['sentences'][0]['parse']))


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
    sentences = ['This is my car.', 'Tom has my car.',
                 'Tom has a house.', 'I got a new car.']

    for i in range(len(sentences)):
        addSentence(sentences[i])
        phrase_per_sent.append(phraseInfo)
        phraseInfo = []
    k = 1
    phr = ""
    count = 0
    for j in range(len(phrase_per_sent)):
        for p in phrase_per_sent[j]:
            phr = p['phrase']
            if j > 0:
                for l in range(count):
                    if my_list[l][2] == p['phrase']:
                        phr = str(my_list[l][0]) + " " + str(my_list[l][3])

                my_list.append([j+1,p['tag'],phr,k])
            else:
                my_list.append([j + 1, p['tag'], phr, k])
            k = k+1
            count = count+1
        k=1
    print(my_list)
    for item in my_list:
        conn.execute('insert into PHRASE_DUPLICATION7 values (?,?,?,?)', (item[0],item[1],item[2],item[3]))
    cursor = conn.execute("SELECT ID, PHRASE_TYPE, PHRASE_TEXT_NUM, PHRASE_ID from PHRASE_DUPLICATION7")
    for row in cursor:
        print("ID = " + str(row[0]))
        print("PHRASE_TYPE = " + row[1])
        print("PHRASE_TEXT_NUM = " + row[2])
        print("PHRASE_ID = " + str(row[3]))






