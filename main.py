#-*- coding:utf-8 -*-
from collections import Counter
import json

def cut(lst, lenth, overlap):
    ret=[]
    inter=lenth-overlap
    for i in range(0,len(lst), inter):
        this_append = []
        for x in lst[i:i+lenth]:
            this_append.append(x)
            if len(this_append)==lenth:
                ret.append(this_append)
    return ret

def get_train_dict(train_path, lenth, overlap):
    all_train = []
    for ll, line in enumerate(open(train_path, 'r', encoding="utf-8")):
        if (ll+1)%100==0:
            print(ll)
        linee = line.strip()
        if 'X' in linee:
            continue
        elif 'U' in linee:
            continue
        elif 'Z' in linee:
            continue
        elif 'B' in linee:
            continue
        elif 'O' in linee:
            continue
        words = cut(linee, lenth, overlap)
        for i in words:
            ii = ''.join(i)
            all_train.append(ii)
    result = Counter(all_train)
    train_dict = dict(result)
    return train_dict

def get_test(test_path, lenth, overlap):
    eg5_test = []
    eg7_test1 = []
    eg7_test2 = []
    for l, x in enumerate(open(test_path,'r',encoding="utf-8")):
        x = x.strip()
        xx = [lst for lst in x]
        post = [str(l) for l in range(1,len(xx)+1)]
        w_post = cut(post, lenth, overlap)
        wordss = cut(x, lenth, overlap)
        if l==0:
            for xxx, y in zip(wordss, w_post):
                xxxx = ''.join(xxx)
                yy = ' '.join(y)
                p = [xxxx, yy]
                eg5_test.append(p)
        if l==1:
            for xxx, o in zip(wordss, w_post):
                xxxx = ''.join(xxx)
                oo = ' '.join(o)
                q = [xxxx, oo]
                eg7_test1.append(q)
        if l==2:
            for xxx, o in zip(wordss, w_post):
                xxxx = ''.join(xxx)
                oo = ' '.join(o)
                q = [xxxx, oo]
                eg7_test2.append(q)
    return eg5_test, eg7_test1, eg7_test2

def get_test_dict(train_dict, eg5_test, eg7_test1, eg7_test2):
    eg5_dict = {}
    eg7_dict1 = {}
    eg7_dict2 = {}
    for a in eg5_test:
        if a[0] not in train_dict.keys():
            eg5_ciping = 0
            eg5_dict[str(a)] = eg5_ciping
        else:
            eg5_ciping = train_dict[a[0]]
            eg5_dict[str(a)] = eg5_ciping
    for aa in eg7_test1:
        if aa[0] not in train_dict.keys():
            eg7_ciping = 0
            eg7_dict1[str(aa)] = eg7_ciping
        else:
            eg7_ciping = train_dict[aa[0]]
            eg7_dict1[str(aa)] = eg7_ciping
    for aa in eg7_test2:
        if aa[0] not in train_dict.keys():
            eg7_ciping = 0
            eg7_dict2[str(aa)] = eg7_ciping
        else:
            eg7_ciping = train_dict[aa[0]]
            eg7_dict2[str(aa)] = eg7_ciping
    return eg5_dict, eg7_dict1, eg7_dict2

def save_cipin(eg5_dict, eg7_dict1,eg7_dict2,lenth,overlap,train_dict):
    with open('result/dict_%s_%s.txt'%(lenth,overlap), 'w', encoding="utf-8")as f, open('result/train_dict_%s_%s.txt'%(lenth,overlap), 'w', encoding="utf-8")as f1:
        leng1 = abs(len(eg7_dict2)-len(eg5_dict))
        leng2 = abs(len(eg7_dict2)-len(eg7_dict1))
        eg5_dict = eg5_dict+['None']*leng1
        eg7_dict1 = eg7_dict1+['None']*leng2
        summ = sum(train_dict.values())
        for eg7_1, eg5, eg7_2 in zip(eg7_dict1,eg5_dict,eg7_dict2):
            f.write(json.dumps(summ) + '\n' + 'EG7_1:\t' + json.dumps(eg7_1) + '\t' + 'EG7_2:\t' + json.dumps(eg7_2) + '\t' + 'EG5:\t' + json.dumps(eg5) + '\n')
        f1.write(json.dumps(train_dict)+'\n')

if __name__=="__main__":
    train_path = 'data/train_36w'
    test_path = 'data/test_loop'
    lenth = input("lenth:")
    lenth = int(lenth)
    overlap = input("overlap:")
    overlap = int(overlap)
    
    train_dict = get_train_dict(train_path, lenth, overlap)
    
    eg5_test, eg7_test1, eg7_test2 = get_test(test_path, lenth, overlap)
    eg5_dict, eg7_dict1, eg7_dict2 = get_test_dict(train_dict, eg5_test, eg7_test1, eg7_test2)
    
    eg5_dict = sorted(eg5_dict.items(), key=lambda x: x[1])
    eg7_dict1 = sorted(eg7_dict1.items(), key=lambda x: x[1])
    eg7_dict2 = sorted(eg7_dict2.items(), key=lambda x: x[1])
    save_cipin(eg5_dict, eg7_dict1,eg7_dict2,lenth,overlap,train_dict)
    