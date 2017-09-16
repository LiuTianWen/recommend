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

    TM = {k: sorted(v, key=lambda d:d[1], reverse=True) for k,v in TM.items()}
    return TM


# topn 邻居数
# recn 推荐数量
def recommend(op_table, sim_metrics, topn, recn):
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
    print(rec[0])
    return rec


# 协同过滤主函数
def cf_main(filename, test_file, topn=20, topk=20):
    sim_name = '-'.join(['sim', str(topn), filename]) + '.txt'
    rec_name = '-'.join(['rec', str(topn), filename]) + '.txt'
    ex_rec_name = '-'.join(['ex_rec', str(topn), str(topk), filename]) + '.txt'
    print('read_table')
    table = read_table(filename)
    sim_fun = functools.partial(similar, table=table)
    import os
    if (os.path.exists(sim_name)):
        print('read sim metrics from file')
        sim_metrics = read_dict(sim_name) 
    else:
        print('cal_metrix')
        sim_metrics = cal_metrix(table, similar_fun=sim_fun)
        write_dict(sim_name, sim_metrics)
    if (os.path.exists(ex_rec_name)):
        print('read recommend result from file')
        rec = read_dict(ex_rec_name)
    else:
        print('recommend')
        rec = recommend(table, sim_metrics, topn, topk)
        write_dict(rec_name, rec)
        exclude_dup(table, rec)
        write_dict(ex_rec_name, rec)
    print('precision')
    print(precision(rec, test_file, topk))
    print('recall')
    print(recall(rec, test_file, topk))


if __name__=='__main__':
    cf_main('trainklnd-Gowalla_totalCheckins.txt',
        'testklnd-Gowalla_totalCheckins.txt',
        topn=10,
        topk=20)

