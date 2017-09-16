#!/usr/bin/python
# coding=utf-8

import numpy as np
import numpy.linalg as la
import rec_lib.svd as svd
import pickle
from rec_lib.utils import *
import os
from rec_lib.similar import * 
from rec_lib.evaluate import * 
from rec_lib import mf
from pprint import pprint



def cal_sim_mat(train_file, featurenum):
    # filename = 'all-trainklnd-Gowalla_totalCheckins.txt'
    dir_name = '-'.join(train_file.split('.')[:-1])
    P_name = dir_name+'/P' 
    Q_name = dir_name+'/Q' 
    sim_mat_name = dir_name+'/sim_mat' 
    if not os.path.exists:
        os.makedirs(dir_name)

    if os.path.exists(sim_mat_name):
        return read_dict(sim_mat_name)

    mat, uid_no, no_uid, iid_no, no_iid = svd.read_table(train_file)
    
    # print(uid_no)

    if os.path.exists(U_name) and os.path.exists(S_name) and os.path.exists(V_name):
        U = read_dict(U_name)
        S = read_dict(S_name)
        V = read_dict(V_name)
    else:
        U, S, V = la.svd(mat)    
        write_dict(U_name,U)
        write_dict(S_name,S)
        write_dict(V_name,V)

    U = U[:,:featurenum]
    # V = V[:featurenum,:]
    # S = np.diag(S[:featurenum])
    # R = np.dot(np.dot(U,S),V)
    sim_mat = {}
    for i in range(len(U)-1):
        for j in range(i+1, len(U)):
            sim = cosine(U[i:i+1], U[j:j+1])
            u1 = no_uid[i]
            u2 = no_uid[j]
            if sim_mat.__contains__(u1):
                sim_mat[u1].append((u2,sim))
            else:
                sim_mat[u1]=[(u2,sim)]
            if sim_mat.__contains__(u2):
                sim_mat[u2].append((u1,sim))
            else:
                sim_mat[u2]=[(u1,sim)]
    write_dict(sim_mat_name, sim_mat)
    return sim_mat

def main_svd(train_file, test_file, featurenum, topns=[20], topks=[20]):
    nprs = []
    nres = []
    print('read_table')
    table = read_table(train_file,uin=0,iin=4,timein=1,scorein=None)
    test = read_table(test_file, uin=0,iin=4,timein=1,scorein=None)
    friends_dic = read_dic_set('Gowalla_edges.txt')

    dir_name = '-'.join(train_file.split('.')[:-1]) + '/'
    sim_fun_name = 'svd'
    
    import os

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    sim_metrics = cal_sim_mat(train_file, featurenum)

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
            # print('precision')
            pr = precision(rec, test, topk)
            print(pr)
            re = recall(rec, test, topk)
            # print('recall')
            # print(re)
            prs.append(float('%.4f' % pr))
            res.append(float('%.4f' % re))
        # print('y1=',prs)
        # print('y2=',res)
        nprs.append(prs.copy())
        nres.append(res.copy())
    return nprs,nres

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
    # print(rec['9232'])
    return rec                       

if __name__ == '__main__':
    nprs, nres = main_svd(train_file='all-trainklnd-Gowalla_totalCheckins.txt',
        featurenum=100,
        test_file='all-testklnd-Gowalla_totalCheckins.txt',
        topns=[5,10,15,20,25,30,100],
        topks=[5,10,15,20,25])
    print(nprs,nres)