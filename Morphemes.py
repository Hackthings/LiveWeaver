#For Creating and Inserting
conn=sqlite3.connect('Morphemes.sqlite')
c=conn.cursor()
c.execute('CREATE TABLE morphemes (morph TEXT, sID INTEGER, wID INTEGER)')
for i in range(len(output['sentences'])):
    for x in output['sentences'][i]['tokens']:
        c.execute('INSERT INTO morphemes(morph,sID,wID) VALUES(?,?,?)',(x['lemma'],i+1,x['index']))

#For Printing
for x in associations:
    table=c.execute('SELECT wID,morph FROM morphemes WHERE sID={v1}'.format(v1=associations[0]))
    for y,z in table:
        if(y==associations[1]):
            print(z)
for x in associations:
    table=c.execute('SELECT wID,morph FROM morphemes WHERE sID={v1}'.format(v1=x[0]))
    for y,z in table:
        print(y,z)