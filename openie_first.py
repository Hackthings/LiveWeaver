from pycorenlp import StanfordCoreNLP
import nltk
from nltk.tree import Tree
ROOT = 'ROOT'
if __name__ == '__main__':
    content = open('mussolini_input.txt')
    content_str = content.read()
    #print(content_str)
    nlp = StanfordCoreNLP('http://10.4.100.141:9000')
    text = (
        content_str)
    output = nlp.annotate(text, properties={
        'annotators': 'tokenize,ssplit,pos,depparse,parse,openie',
        'outputFormat': 'json'
    })
    #print(output["sentences"][0]['openie'][0]['relation'])
    '''t = Tree.fromstring(output['sentences'][0]['parse'])
    t.draw()
    t.pretty_print()'''
    def check_is(string):
        switcher={
            "is":True,
            "am":True,
            "was":True,
            "were":True}
        return switcher.get(string,False)

    def check_inheritance(output):
        #print("enter") #debugging check
        inher_list={}
        if output == []:
            return "Empty"   #debugging checks; can be replaced by None or any other stmt
        else:
            if check_is(output["relation"]) == False:
                return "Not is-a"  #debugging checks; can be replaced by None or any other stmt
            else:
                inher_list['Parent']=output['object']
                inher_list['relation'] = output['relation']
                inher_list['Child']=output['subject']
                return inher_list
            
    #dict1 = check_inheritance(output["sentences"][0]["openie"][0])
    #print(dict1)            
    
    solution = []
    for sentence in output['sentences']:
        for op in sentence["openie"]:
            dict1 = check_inheritance(op);
            print(dict1)
            solution.append(dict1)
                    
    content_str = content_str.split('\n')
    #print(len(content_str))
    #print(len(solution))
    file = open("relations.txt","w")
    for i in range(len(solution)):
        file.write(str(solution[i]))
        file.write("\n")


    
