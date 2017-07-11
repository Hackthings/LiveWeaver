import requests
from bs4 import BeautifulSoup
import sqlite3
reader=open('ConceptNetWords.txt','r+')
conn=sqlite3.connect('connet.sqlite')
c=conn.cursor()
c.execute('CREATE TABLE LEAVES (leaf TEXT)')
proxies = {
	'https': 'socks5://111.198.2.90:1080'
}
words=[word.replace("\n", "") for word in reader.readlines()]
for word in words:
    r=requests.get('http://conceptnet.io/c/en/{}?rel=/r/IsA&limit=1000'.format(word),proxies=proxies)
    soup=BeautifulSoup(r.content,'html.parser')
    flag=1
    for x in soup.find_all('span'):
        if(x.a!=None):
            concept=(x.a.attrs['href'])[6:]
            if(concept==word):
                flag=0
    if(flag==1):
        print(word)
        c.execute('INSERT INTO LEAVES(leaf) VALUES(?)',(word,))