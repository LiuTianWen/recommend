# -*- coding:utf-8 -*-  
from datetime import datetime

import numpy as np
from numpy import *
import pickle


# 进度条
def view_bar(num, total):
    rate = num / total
    rate_num = int(rate * 100)
    print(rate_num)


# 字典按照value排序
def sort_dict(dic, reverse=True):
    return sorted(dic.items(), key=lambda d: d[1], reverse=reverse)


# 读取评分表 user, item, score
def read_checks_table(filename, split_sig='\t', uin=0, iin=4, scorein=None, timein=1):
    table = {}
    with open(filename) as f:
        for each in f:
            elements = each.strip().split(split_sig)
            u = elements[uin]
            i = elements[iin]
            score = 1 if scorein is None else elements[scorein]
            _time = None if timein is None else datetime.strptime(elements[timein], '%Y-%m-%dT%H:%M:%SZ')
            if table.get(u) is not None:
                table[u].append((i, score, _time))
            else:
                table[u] = [(i, score, _time)]
    return table


# 读 文件
def read_obj(filename, root=''):
    with open(root + filename, 'rb') as f:
        return pickle.load(f)


# 写 文件
def write_obj(filename, dic, root=''):
    with open(root + filename, 'wb') as f:
        pickle.dump(dic, f)


# 读取列表归属字典（朋友集合等）
def read_dic_set(filename):
    dic_f = {}
    with open(filename) as f:
        for each in f:
            es = each.strip().split('\t')
            u1 = es[0]
            u2 = es[1]
            if dic_f.__contains__(u1):
                dic_f[u1].add(u2)
            else:
                dic_f[u1] = {u2}
    return dic_f


def dic_value_reg_one(obj):
    if not isinstance(obj, dict):
        raise RuntimeError('type error')
    values = list(obj.values())
    s = sum(values)
    for k in obj.keys():
        obj[k] = obj[k] / s


# 推荐结果去重
def exclude_dup(op_table, rec):
    for k in rec.keys():
        old_items = set([i[0] for i in op_table.get(k, [])])
        rec[k] = [e for e in rec[k] if not old_items.__contains__(e[0])]


# 读取评分表 user, item, score
def read_checks_mat(filename, split_sig='\t', uin=0, iin=4, scorein=None, timein=1):
    uid_no = {}
    iid_no = {}
    no_uid = {}
    no_iid = {}
    uid = 0
    iid = 0
    table = {}
    with open(filename) as f:
        for each in f:
            elements = each.strip().split(split_sig)
            u = elements[uin]
            i = elements[iin]
            score = 1 if scorein is None else elements[scorein]
            _time = None if timein is None else datetime.strptime(elements[timein], '%Y-%m-%dT%H:%M:%SZ')
            if not uid_no.__contains__(u):
                uid_no[u] = uid
                no_uid[uid] = u
                uid += 1
            u = uid_no[u]
            if not iid_no.__contains__(i):
                iid_no[i] = iid
                no_iid[iid] = i
                iid += 1
            i = iid_no[i]
            if table.get(u) is not None:
                table[u].append((i, score, _time))
            else:
                table[u] = [(i, score, _time)]
    mat = np.zeros((len(uid_no), len(iid_no)))
    for u, its in table.items():
        for it in its:
            mat[u][it[0]] = it[1]

    return mat, uid_no, no_uid, iid_no, no_iid


if __name__ == '__main__':
    a = {1: 2, 3: 6}
    dic_value_reg_one(a)
    print(a)
