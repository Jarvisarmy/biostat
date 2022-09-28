#-*- coding:utf-8 -*-
from collections import Counter
import json
import os
from pathlib import Path

def cut(lst, length, overlap):
    ret=[]
    inter=length-overlap
    for i in range(0,len(lst), inter):
        this_append = []
        for x in lst[i:i+length]:
            this_append.append(x)
            if len(this_append)==length:
                ret.append(this_append)
    return ret

def save_train_dict(dict_data, save_path):
    with open(save_path,'w',encoding='utf-8') as f:
        for k, v in dict_data.items():
            f.write("%s\t%d\n" % (k,v))
      
def load_train_dict(save_path):
    dict_data = dict()
    num = 0
    if not os.path.exists(save_path): return {}
    with open(save_path, 'r+', encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n')
            items = line.split('\t')
            num +=1
            try:
                dict_data[items[0]] = int(items[1])
            except IndexError:
                logger.error('IndexError, index:%s, line%s' %(num,line))
    return dict_data
def save_res_dict(dict_data, save_path):
    with open(save_path,'w',encoding='utf-8') as f:
        for k, [c,count] in dict_data.items():
            f.write("%s\t%s\t%d\n" % (k,c,count))
def get_train_dict(result_path,train_path_list, length, overlap):
    all_train = []
    total = 0
    train_dict = load_train_dict(result_path)
    for train_path in train_path_list:
        total_path = 0
        for ll, line in enumerate(open(train_path, 'r')):#, encoding="utf-8")):
            total_path = ll
            #if (ll+1)%100==0:
            #    print(ll)
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
            words = cut(linee, length, overlap)
            for i in words:
                ii = ''.join(i)
                if ii in train_dict:
                    train_dict[ii] += 1
                else:
                    train_dict[ii] = 1
        total += total_path
        print("the number of lines processed: ",total)
    save_train_dict(train_dict, result_path)
    
    return train_dict

def get_test(test_path, length, overlap):
    res = []
    for ll, line in enumerate(open(test_path,'r',encoding='utf-8')):
        line = line.strip()
        pos = [str(l) for l in range(1,len(line)+1)]
        poss = cut(pos,length,overlap)
        lines = cut(line,length,overlap)
        temp_res = []
        for line, pos in zip(lines, poss):
            line = ''.join(line)
            pos = ' '.join(pos)
            temp_res.append([line, pos])
        res.append(temp_res)
    return res[0],res[1]

def get_test_dict(train_dict, eg5_test, eg7_test):
    eg5_dict = {}
    eg7_dict = {}
    for a in eg5_test:
        if a[0] not in train_dict.keys():
            eg5_ciping = 0
            eg5_dict[str(a)] = eg5_ciping
        else:
            eg5_ciping = train_dict[a[0]]
            eg5_dict[str(a)] = eg5_ciping
    for aa in eg7_test:
        if aa[0] not in train_dict.keys():
            eg7_ciping = 0
            eg7_dict[str(aa)] = eg7_ciping
        else:
            eg7_ciping = train_dict[aa[0]]
            eg7_dict[str(aa)] = eg7_ciping
    return eg5_dict, eg7_dict


def get_mutation_dict(data,path):
    mutation_dict = {}
    for token, count in data:
        token = token[1:-1]
        word, indexes = token.split(',')
        word = word[1:-1]
        indexes = indexes[2:-1]
        indexes = indexes.split()
        for c, index in zip(word,indexes):
            if index in mutation_dict:
                mutation_dict[index][1] += count
            else:
                mutation_dict[index] = [c,count]
    mutation_dict = dict(sorted(mutation_dict.items(),key=lambda item: item[1][1]))
    save_res_dict(mutation_dict,path)
        
if __name__=="__main__":
    
    
    length = input("length:")
    length = int(length)
    overlap = input("overlap:")
    overlap = int(overlap)
    train_path = 'result/train_dict_%s_%s.txt'%(length,overlap)
    test_path = 'data/test_loop'
    eg5_res_path = 'result/eg5_res_dict_%s_%s.txt'%(length,overlap)
    eg7_res_path = 'result/eg7_res_dict_%s_%s.txt'%(length,overlap)
    
    train_path_list = [
        "data/SwissProt.txt",
        "data/TrEMBL_Athailana.txt",
        "data/TrEMBL_BarbusGrahami.txt",
        "data/TrEMBL_Bovine.txt",
        "data/TrEMBL_BrownTrout.txt",
        "data/TrEMBL_Carp.txt",
        "data/TrEMBL_CohoSalmon.txt",
        "data/TrEMBL_EpeiraVentricosa.txt",
        "data/TrEMBL_FruitFly.txt",
        "data/TrEMBL_Goatgrass.txt",
        "data/TrEMBL_Grape.txt",
        "data/TrEMBL_Human.txt",
        "data/TrEMBL_Kapabacteria.txt",
        "data/TrEMBL_Mouse.txt",
        "data/TrEMBL_part1.txt",
        "data/TrEMBL_part2.txt",
        "data/TrEMBL_part3.txt",
        "data/TrEMBL_part4.txt",
        "data/TrEMBL_Rat.txt",
        "data/TrEMBL_Rice.txt",
        "data/TrEMBL_TrifoliumMedium.txt",
        "data/TrEMBL_TriticumDurum.txt",
        "data/TrEMBL_Trout.txt",
        "data/TrEMBL_Wheat.txt",
        "data/TrEMBL_Zebrafish.txt"
    ]
    eg5 = "MET ASN LYS SER VAL ALA PRO LEU LEU LEU ALA ALA SER ILE LEU TYR GLY GLY ALA ALA ALA GLN GLN THR VAL TRP GLY GLN CYS GLY GLY ILE GLY TRP SER GLY PRO THR ASN CYS ALA PRO GLY SER ALA CYS SER THR LEU ASN PRO TYR TYR ALA GLN CYS ILE PRO GLY ALA THR THR ILE THR THR SER THR ARG PRO PRO SER GLY PRO THR THR THR THR ARG ALA THR SER THR SER SER SER THR PRO PRO THR SER SER GLY VAL ARG PHE ALA GLY VAL ASN ILE ALA GLY PHE ASP PHE GLY CYS THR THR ASP GLY THR CYS VAL THR SER LYS VAL TYR PRO PRO LEU LYS ASN PHE THR GLY SER ASN ASN TYR PRO ASP GLY ILE GLY GLN MET GLN HIS PHE VAL ASN ASP ASP GLY MET THR ILE PHE ARG LEU PRO VAL GLY TRP GLN TYR LEU VAL ASN ASN ASN LEU GLY GLY ASN LEU ASP SER THR SER ILE SER LYS TYR ASP GLN LEU VAL GLN GLY CYS LEU SER LEU GLY ALA TYR CYS ILE VAL ASP ILE HIS ASN TYR ALA ARG TRP ASN GLY GLY ILE ILE GLY GLN GLY GLY PRO THR ASN ALA GLN PHE THR SER LEU TRP SER GLN LEU ALA SER LYS TYR ALA SER GLN SER ARG VAL TRP PHE GLY ILE MET ASN GLU PRO HIS ASP VAL ASN ILE ASN THR TRP ALA ALA THR VAL GLN GLU VAL VAL THR ALA ILE ARG ASN ALA GLY ALA THR SER GLN PHE ILE SER LEU PRO GLY ASN ASP TRP GLN SER ALA GLY ALA PHE ILE SER ASP GLY SER ALA ALA ALA LEU SER GLN VAL THR ASN PRO ASP GLY SER THR THR ASN LEU ILE PHE ASP VAL HIS LYS TYR LEU ASP SER ASP ASN SER GLY THR HIS ALA GLU CYS THR THR ASN ASN ILE ASP GLY ALA PHE SER PRO LEU ALA THR TRP LEU ARG GLN ASN ASN ARG GLN ALA ILE LEU THR GLU THR GLY GLY GLY ASN VAL GLN SER CYS ILE GLN ASP MET CYS GLN GLN ILE GLN TYR LEU ASN GLN ASN SER ASP VAL TYR LEU GLY TYR VAL GLY TRP GLY ALA GLY SER PHE ASP SER THR TYR VAL LEU THR GLU THR PRO THR GLY SER GLY ASN SER TRP THR ASP THR SER LEU VAL SER SER CYS LEU ALA ARG LYS GLY"
    eg7 = "MET ALA PRO SER VAL THR LEU PRO LEU THR THR ALA ILE LEU ALA ILE ALA ARG LEU VAL ALA ALA GLN GLN PRO GLY THR SER THR PRO GLU VAL HIS PRO LYS LEU THR THR TYR LYS CYS THR LYS SER GLY GLY CYS VAL ALA GLN ASP THR SER VAL VAL LEU ASP TRP ASN TYR ARG TRP MET HIS ASP ALA ASN TYR ASN SER CYS THR VAL ASN GLY GLY VAL ASN THR THR LEU CYS PRO ASP GLU ALA THR CYS GLY LYS ASN CYS PHE ILE GLU GLY VAL ASP TYR ALA ALA SER GLY VAL THR THR SER GLY SER SER LEU THR MET ASN GLN TYR MET PRO SER SER SER GLY GLY TYR SER SER VAL SER PRO ARG LEU TYR LEU LEU ASP SER ASP GLY GLU TYR VAL MET LEU LYS LEU ASN GLY GLN GLU LEU SER PHE ASP VAL ASP LEU SER ALA LEU PRO CYS GLY GLU ASN GLY SER LEU TYR LEU SER GLN MET ASP GLU ASN GLY GLY ALA ASN GLN TYR ASN THR ALA GLY ALA ASN TYR GLY SER GLY TYR CYS ASP ALA GLN CYS PRO VAL GLN THR TRP ARG ASN GLY THR LEU ASN THR SER HIS GLN GLY PHE CYS CYS ASN GLU MET ASP ILE LEU GLU GLY ASN SER ARG ALA ASN ALA LEU THR PRO HIS SER CYS THR ALA THR ALA CYS ASP SER ALA GLY CYS GLY PHE ASN PRO TYR GLY SER GLY TYR LYS SER TYR TYR GLY PRO GLY ASP THR VAL ASP THR SER LYS THR PHE THR ILE ILE THR GLN PHE ASN THR ASP ASN GLY SER PRO SER GLY ASN LEU VAL SER ILE THR ARG LYS TYR GLN GLN ASN GLY VAL ASP ILE PRO SER ALA GLN PRO GLY GLY ASP THR ILE SER SER CYS PRO SER ALA SER ALA TYR GLY GLY LEU ALA THR MET GLY LYS ALA LEU SER SER GLY MET VAL LEU VAL PHE SER ILE TRP ASN ASP ASN SER GLN TYR MET ASN TRP LEU ASP SER GLY ASN ALA GLY PRO CYS SER SER THR GLU GLY ASN PRO SER ASN ILE LEU ALA ASN ASN PRO ASN THR HIS VAL VAL PHE SER ASN ILE ARG TRP GLY ASP ILE GLY SER THR THR ASN SER THR ALA PRO PRO PRO PRO PRO ALA SER SER THR THR PHE SER THR THR ARG ARG SER SER THR THR SER SER SER PRO SER CYS THR GLN THR HIS TRP GLY GLN CYS GLY GLY ILE GLY TYR SER GLY CYS LYS THR CYS THR SER GLY THR THR CYS GLN TYR SER ASN ASP TYR TYR SER GLN CYS LEU"
    train_dict = get_train_dict(train_path,train_path_list, length, overlap)
    #train_dict = load_train_dict(train_path)
    eg5_test, eg7_test = get_test(test_path, length, overlap)
    eg5_dict, eg7_dict = get_test_dict(train_dict, eg5_test, eg7_test)
    
    eg5_dict = sorted(eg5_dict.items(), key=lambda x: x[1])
    eg7_dict = sorted(eg7_dict.items(), key=lambda x: x[1])
    get_mutation_dict(eg5_dict,eg5_res_path)
    get_mutation_dict(eg7_dict,eg7_res_path)
    
    