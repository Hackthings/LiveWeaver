from pycorenlp import StanfordCoreNLP
import nltk
from nltk.tree import ParentedTree
import sqlite3
conn= sqlite3.connect('phrase_test1.db')
conn.execute('CREATE TABLE ZEROPF(S_ID BIGINT NOT NULL,T_ID BIGINT NOT NULL,TAG TEXT,PHRASE TEXT, PRIMARY KEY(S_ID,T_ID))')
print("Success")
ROOT = 'ROOT'
if __name__ == '__main__':
    def addSentence(sentence,id):
        output = nlp.annotate(sentence, properties={
            'annotators': 'parse',
            'outputFormat': 'json'
        })
        assignPhrases(ParentedTree.fromstring(output['sentences'][0]['parse']),id)
        
    
    def checkBeforeInsert(phraseInfo,id):
        
        cursor = conn.execute("SELECT * FROM ZEROPF Where TAG = ? AND PHRASE = ?",(phraseInfo['tag'],phraseInfo['phrase']))
        data = cursor.fetchall()
        if len(data)==0:
            print('loop1')
            global INDEX
            conn.execute('INSERT INTO ZEROPF(S_ID,T_ID,TAG,PHRASE) values (?,?,?,?)',(id,INDEX,phraseInfo['tag'],phraseInfo['phrase']))
            INDEX = INDEX + 1
            
        else:
            print(data[0][0:2])
            print(str(data[0][0:2])[1:-1])
            conn.execute('INSERT INTO ZEROPF(S_ID,T_ID,TAG,PHRASE) values (?,?,?,?)',(id,INDEX,phraseInfo['tag'],str(data[0][0:2])))        
            INDEX +=1
            
        
    def assignPhrases(t,id):
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
                print(phraseInfo)
                checkBeforeInsert(phraseInfo,id)
                # send this to database
            if t.height() == 2:  # child nodes
                return

            for child in t:
                assignPhrases(child,id)

    nlp = StanfordCoreNLP('http://10.4.100.141:9000')

    phraseTags = ['ADJP', 'ADVP', 'CONJP', 'FRAG', 'INTJ', 'LST', 'NAC', 'NP', 'NX', 'PP', 'PRN', 'PRT', 'QP',
                  'RRC', 'UCP', 'VP', 'WHADJP', 'WHAVP', 'WHNP', 'WHPP', 'X']
    # get sentence file as list of sentences
    # test data assigned for now
    sentences = ['This is my car.','Tom applied for the job.','Tom went back to his hometown.',
                 'I got a new camera.', 'I went out in my car.'
                 ]
    
    for i in range(0,len(sentences)):
        INDEX =0
        addSentence(sentences[i],i)
        #print(i)
print("reached cursor")

cursor = conn.execute("SELECT * FROM ZEROPF")

for row in cursor:
    print(row)
conn.commit()
conn.close()