from pycorenlp import StanfordCoreNLP
import nltk
from nltk.tree import ParentedTree
ROOT = 'ROOT'
if __name__ == '__main__':

    # print(output['sentences'][0]['openie'][0]['relation'])
    '''t = Tree.fromstring(output['sentences'][0]['parse'])
    t.draw()
    t.pretty_print()'''

    def checkFromTree(t, curr=False):
        inher_list={}
        if curr == True:
            return curr,inher_list
        try:
            t.label()
        except AttributeError:
            return curr
        else:
            if 'VB'in t.label():
                if t.right_sibling() != None:
                    if t.right_sibling().label() == 'NP':
                        inher_list['Parent']=t.right_sibling().leaves()                        
                        inher_list['Relation'] =t.leaves()
                        inher_list['Child']=t.parent().left_sibling().leaves()
                        print(inher_list)
                        curr = True
                return curr

            if t.height() == 2:  # child nodes
                return curr

            for child in t:
                curr = checkFromTree(child, curr)
            return curr

    def check_is(string):
        switcher = {
            'is': True,
            'am': True,
            'was': True,
            'were': True,
            "'m": True}
        return switcher.get(string, False)

    def check_inheritance(output):
        # print('enter') #debugging check
        if output['openie'] == []:
            return 'Not an is-a'  # debugging checks; can be replaced by None or any other stmt
        else:
            result = check_is(output['openie'][0]['relation'])
            if result == False:
                return 'Not an is-a'  # debugging checks; can be replaced by None or any other stmt
            else:
                if checkFromTree(ParentedTree.fromstring(output['parse'])):
                    return None
                else:
                    return 'Not an is-a'

    
    nlp = StanfordCoreNLP('http://10.4.100.141:9000')
    text = ('She is a dancer. I am a doctor. He had lunch. I am fine.')
    output = nlp.annotate(text, properties={
        'annotators': 'tokenize,ssplit,pos,depparse,parse,openie',
        'outputFormat': 'json'
    })

    solution = []

    for sentence in output['sentences']:
        resp = check_inheritance(sentence)
        if resp==None:
            continue
        else:
            print(resp)
        
    '''for op in sentence['parse']:
        response = check_inheritance(op)
        print(response)
        solution.append(response)
                    
    content_str = content_str.split('\n')
    #print(len(content_str))
    #print(len(solution))'''

    