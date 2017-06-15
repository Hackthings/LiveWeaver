from pycorenlp import StanfordCoreNLP
import nltk
from nltk.tree import ParentedTree
import psycopg2
import wikipedia
from nltk.tokenize import sent_tokenize

ROOT = 'ROOT'
if __name__ == '__main__':

    phraseTags = ['ADJP', 'ADVP', 'CONJP', 'FRAG', 'INTJ', 'LST', 'NAC', 'NP', 'NX', 'PP', 'PRN', 'PRT', 'QP',
                  'RRC', 'UCP', 'VP', 'WHADJP', 'WHAVP', 'WHNP', 'WHPP', 'X']
    connector = psycopg2.connect(database = "zero", user = "postgres", password = "zero", host = "10.4.100.123", port = "5432")
    conn = connector.cursor()
    conn.execute("CREATE TABLE WORD_INDEX_PARA(P_ID INT NOT NULL,SEN_ID INT NOT NULL, PHRASE_ID INT NOT NULL, WORD_ID INT NOT NULL,  FOREIGN KEY(P_ID) REFERENCES P_INDEX(P_ID));")

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

    conn.execute("CREATE TABLE P_INDEX(P_ID INT NOT NULL AUTOINCREMENT,NAMESCOPE TEXT,CONTEXT TEXT, P_TXT TEXT );")

    '''for i in range(40):
        namescopes = []
        nmscp = wikipedia.random()
        namescopes.append(nmscp)
        articles_names=wikipedia.search(namescopes[i],results=1000)
        for j in range(10000):
            articles = []
            articles.append(articles_names[j].summary())
            conn.execute('INSERT INTO P_INDEX(NAMESCOPE,CONTEXT,P_TXT) VALUES(?,?,?)',(nmscp,articles_names[j].title,articles[j]))'''

        # test data assigned for now
        
        k = 0
        dict = {}
        flag = 0

        for k in range(len(articles)):
            sentences = sent_tokenize(articles[k])
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
                #Making the table containing phrases
            for j in range(len(phrase_per_sent)):
                for i,p in enumerate(phrase_per_sent[j]):
                    for n in range(len(p['phrase'].split())):
                        wid = dict.get(p['phrase'].split()[n])
                        my_list.append([k+1,j+1,i+1,wid+1])
        for item in my_list:
            conn.execute('insert into WORD_INDEX_PARA values (?,?,?,?)', (item[0],item[1],item[2],item[3]))
        conn.execute("SELECT * from WORD_INDEX_PARA")
        rows = conn.fetchall()
        for row in rows:
            print(row)

            
    conn.commit()
    conn.close()




