import math
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from random import random   
import sys
import functools
from datetime import datetime
import pickle
from rec_lib.utils import *
from rec_lib.similar import *
from rec_lib.evaluate import *


# 计算相似度矩阵，
# {
#  u1:[(u2, s12), (u3, s13)}, 
#  u2:[(u1, s21), (u3, s23],
#  u3:[(u1, s31), (u2, s32)]
# }
def cal_metrix(table, similar_fun=sequece_score):
    count = 0
    ids = list(table.keys())
    total = len(ids)*len(ids)
    l = len(ids)
    print(l)
    TM = {}
    for u1 in ids:
        if not TM.__contains__(u1):
            TM[u1] = []
        for u2 in ids:
            if u1 == u2:
                continue
            else:
                count += 1
                if count % 10000 == 0:
                    view_bar(count, total)
                TM[u1].append((u2, similar_fun(u2, u1)))

        sum_score = sum([e[1] for e in TM[u1]])
        if sum_score > 0:
            TM[u1] = [[e[0], e[1]/sum_score] for e in TM[u1]]

    TM = {k: sorted(v, key=lambda d:d[1], reverse=True) for k,v in TM.items()}

    return TM


# topn 邻居数
# recn 推荐数量
def recommend(op_table, sim_metrics, topn):

    rec = {}
    for u in sim_metrics:
        count = 0
        rec[u] = {}
        for uss in sim_metrics[u]:
            count += 1
            if count >= topn:
                break
            for (item, score, time) in op_table[uss[0]]:
                if rec[u].keys().__contains__(item):
                    rec[u][item] += score*uss[1]
                else:
                    rec[u][item] = score*uss[1]
    for user in rec.keys():
        rec[user] = sort_dict(rec[user])
    # print(rec[0])
    return rec


# 协同过滤主函数
def cf_main(train_file, test_file, topns=[20], topks=[20]):
    nprs = []
    nres = []
    print('read_table')
    table = read_table(train_file,uin=0,iin=4,timein=1,scorein=None)
    test = read_table(test_file, uin=0,iin=4,timein=1,scorein=None)
    friends_dic = read_dic_set('Gowalla_edges.txt')
    # sim_fun1 = social_similar(friends_dic)
    # sim_fun1 = sequece_similar(table, friends_dic, sequece_score(table))
    sim_fun = cosine_similar(table)
    # sim_fun = lambda x,y:0.1*sim_fun1(x,y)+0.9*sim_fun2(x,y)
    sim_fun_name =  sim_fun.name #'soc_locsq'#
    dir_name = '-'.join(train_file.split('.')[:-1]) + '/'
    sim_name = dir_name + '-'.join(['sim', sim_fun_name , train_file])
    
    import os

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    if (os.path.exists(sim_name)):
        print('read sim metrics from file')
        sim_metrics = read_dict(sim_name) 
    else:
        print('cal_metrix')
        sim_metrics = cal_metrix(table, similar_fun=sim_fun)
        write_dict(sim_name, sim_metrics)
    for topn in topns:
        rec_name = dir_name + '-'.join(['rec', sim_fun_name, str(topn), train_file])
        ex_rec_name = dir_name + '-'.join(['ex_rec', sim_fun_name, str(topn), train_file])
        if (os.path.exists(ex_rec_name)):
            print('read recommend result from file')
            rec = read_dict(ex_rec_name)
        else:
            print('recommend')
            rec = recommend(table, sim_metrics, topn)
            write_dict(rec_name, rec)
            exclude_dup(table, rec)
            write_dict(ex_rec_name, rec)

        prs = []
        res = []
        for topk in topks:
            print('precision')
            pr = precision(rec, test, topk)
            print(pr)
            re = recall(rec, test, topk)
            print('recall')
            prs.append(float('%.4f' % pr))
            res.append(float('%.4f' % re))
        # print('y1=',prs)
        # print('y2=',res)
        nprs.append(prs.copy())
        nres.append(res.copy())
    return nprs,nres

if __name__=='__main__':
    nprs, nres = cf_main('trainklnd-Gowalla_totalCheckins.txt',
        'testklnd-Gowalla_totalCheckins.txt',
        topns=[5,10,15,20,25,30],
        topks=[5,10,15,20,25])
    print (nprs,nres)

