# -*- coding:utf-8 -*-  
import numpy as np
from datetime import datetime
from numpy import linalg
# 读取评分表 user, item, score
def read_mat(filename, split_sig='\t', uin=0, iin=4, scorein=None, timein=1):
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
    H = [
            [3.16991321031250,52.4425641326457,2.73475152482102],
            [-8.76695007100685,43.4831885343255,-37.1705395356264],
            [-1.59218748085971,-24.3510937156625,12.8339630267640],
        ]
    U,S,V = linalg.svd(H)
    print(U)
    print(S)
    print(V)
    print(np.dot(np.dot(U,np.diag(S)),V))
    