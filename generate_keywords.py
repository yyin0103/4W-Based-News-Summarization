

# set up spacy's ner and text rank
import spacy
from spacy import displacy
import pytextrank
from collections import defaultdict
import argparse

def manual(text, max_num):
    
    all_entities = ['ORG', 'PERSON', 'GPE', 'DATE', 'CARDINAL', 'NORP', 'ORDINAL', 'LOC', \
                    'WORK_OF_ART', 'MONEY', 'TIME', 'EVENT', 'PRODUCT', 'FAC', 'QUANTITY', \
                    'PERCENT', 'LANGUAGE', 'LAW'] 
    important = ["PERSON", "GPE", "ORG", "CARDINAL", "DATE", "NORP", "MONEY", "WORK_OF_ART"]
    
    
    doc = nlp(text)
    
    d = {}
    
    # get entites
    res = []
    text_d = defaultdict(str)
    text_count = defaultdict(int)
    entity_d = defaultdict(list)
    
    for ent in doc.ents:
        text_d[ent.text] = ent.label_
        text_count[ent.text] += 1
        entity_d[ent.label_].append(ent.text) 
            
    # get text rank
    record = set()
    rank_score = []
    for phrase in doc._.phrases:
        
        if phrase.rank < 0.01:
            break
        rank_score.append(phrase.rank)
        
        if phrase.text in text_d: 
            if text_d[phrase.text] in all_entities:
                all_entities.remove(text_d[phrase.text])
                
            d[phrase.text] = [text_d[phrase.text], phrase.rank, phrase.count, entity_weight[text_d[phrase.text]], 0.3 * phrase.rank + 0.7 * entity_weight[text_d[phrase.text]]]
        
        else:
            
            d[phrase.text] = [None, phrase.rank, phrase.count, mean,  mean]
    
    try:
        mean_score = sum(rank_score)/len(rank_score)
        
    except Exception:
        pass

    # check if there's any leftovers                                                 
    for ent in important:
        if ent in all_entities and ent in entity_d.keys():
            for word in entity_d[ent]:
                # last phrase rank                                                       
                d[word] = [ent, 0.009, text_count[word], entity_weight[ent], \
                           0.3 * 0.009  + 0.7 * entity_weight[ent]]


    res = [(k, v) for k, v in d.items()]
    res = sorted(res, key=lambda x: x[-1], reverse=True)[:max_num]

    return [x[0] for x in res]

nlp = spacy.load("en_core_web_sm")
nlp.get_pipe("ner")
nlp.add_pipe("textrank")

entity_weight = {
'PERSON':     0.090851 * 0.65,
'LOC':        0.089072 * 0.66,
'FAC':        0.089031 * 0.67,
'GPE':        0.088363 * 0.68,
'ORG':        0.084918 * 0.68,
'EVENT':      0.084812,
'NORP':       0.084434,
'ORDINAL':    0.080775,
'LANGUAGE':   0.079413,
'PRODUCT':    0.078703,
'WORK_OF_ART': 0.077155,
'DATE':        0.070339,
'TIME':        0.067215 ,
'LAW':         0.065685 * 1.1,
'PERCENT':     0.057107 * 1.2,
'QUANTITY':    0.055759 * 1.3,
'CARDINAL':    0.046437 * 1.4,
'MONEY':       0.028131 * 1.5,}

mean = min(entity_weight.values())

if __name__ == '__main__':
    

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--data_path', type=str,
                        help='path of the document')
    parser.add_argument('--method', type=str, 
                        help='method to extract keywords')
    parser.add_argument('--max_num', type=int,
                        help='the number of keywords to extract')
    parser.add_argument('--output_path', type=str, nargs='+',
                        help='output path of the text file')
   
    args = parser.parse_args()


    res = open(args.output_path,"w")
    with open(args.data_path, 'r') as f:
        for doc in f:
            f.write(manual(doc, args.max_num))




