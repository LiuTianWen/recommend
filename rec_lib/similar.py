import math
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from random import random
import sys
import functools
from datetime import datetime
import pickle
import numpy.linalg as linalg
from numpy import matrix
from numpy import array


class cosine_similar:
    name = 'cosin'

    def __init__(self, table):
        self.table = table

    def __call__(self, u1, u2):
        x = self.table[u1]
        y = self.table[u2]
        mx = {e[0] for e in x}
        my = {e[0] for e in y}
        downx = len(mx)
        downy = len(my)
        up = sum([1 for k in set(mx) & set(my)])
        # print(up)
        return math.sqrt(up * up / (downx * downy))


# how many times u2 followed u1
# delta: time_limit
class sequece_score:
    def __init__(self, table, delta=24 * 60 * 60):
        self.table = table
        self.delta = delta

    @property
    def name(self):
        return 'sq_score' + str(self.delta)

    def __call__(self, u1, u2):
        x = self.table[u1]
        y = self.table[u2]
        mx = {}
        for e in x:
            if not mx.__contains__(e[0]):
                mx[e[0]] = e[2]
        my = {}
        for e in y:
            if not my.__contains__(e[0]):
                my[e[0]] = [e[2], e[1]]
            else:
                my[e[0]][1] += e[1]
        up = 0
        for k, v in my.items():
            if mx.get(k) and v[0].__ge__(mx[k]) and 0 <= ((v[0] - mx[k]).seconds) < self.delta:
                up += 1
        return up


class social_similar:
    name = 'edge'

    def __init__(self, friends_dic):
        self.friends_dic = friends_dic

    def __call__(self, u1, u2):
        up = len(set(self.friends_dic.get(u1, set())) & self.friends_dic.get(u2, set()))
        down = len(self.friends_dic.get(u1, set()))
        if down:
            return up / down
        else:
            return 0


class social_and_similar:
    name = 'soc_loc'

    def __init__(self, friends_dic, table, rate=0.5):
        self.friend_similar = social_similar(friends_dic)
        self.cosine_similar = cosine_similar(table)
        self.rate = rate

    def __call__(self, u1, u2):
        fs = self.friend_similar(u1, u2)
        cs = self.cosine_similar(u1, u2)
        return rate * fs + (1 - self.rate) * cs


class sequece_similar:
    name = 'sqs'

    def __init__(self, table, friends_dic, similar_fun):
        self.friends_dic = friends_dic
        count = 0
        ids = list(table.keys())
        total = len(ids) * len(ids)
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
                        print(count)
                    TM[u1].append((u2, similar_fun(u2, u1)))

            sum_score = sum([e[1] for e in TM[u1]])
            if sum_score > 0:
                TM[u1] = [[e[0], e[1] / sum_score] for e in TM[u1]]
        self.TM = TM

    def save(filename):
        saveTM = {k: sorted(v, key=lambda d: d[1], reverse=True) for k, v in TM.items()}

    def __call__(self, u1, u2):
        try:
            if self.friends_dic[u1].__contains__(u2):
                return self.TM[u1][u2]
            else:
                return 0
        except:
            return 0

# for mat
def cosine(A, B):
    try:
        num = float(np.dot(A, B.T))  # 若为行向量则 A * B.T
        denom = linalg.norm(A) * linalg.norm(B)
        cos = num / denom  # 余弦值
        sim = 0.5 + 0.5 * cos  # 归一化
    except Exception as e:
        print(A, len(A), len(A[0]), type(A))
        print(B, len(B), len(B[0]), type(B))
        return 0
    return sim

def consine_for_dic(dx, dy):
        down1 = sum([v*v for v in dx.values()])
        down2 = sum([v*v for v in dy.values()])
        up = 0
        for k in dx.keys():
            up += dx.get(k, 0) * dy.get(k, 0)
        return up/math.sqrt(down1 * down2)


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
                    print(count, total)
                TM[u1].append((u2, similar_fun(u2, u1)))

        sum_score = sum([e[1] for e in TM[u1]])
        if sum_score > 0:
            TM[u1] = [[e[0], e[1]/sum_score] for e in TM[u1]]

    TM = {k: sorted(v, key=lambda d:d[1], reverse=True) for k,v in TM.items()}

    return TM


if __name__ == '__main__':
    A = array([[1,2,3]])
    B = array([[1,2,3]])
    print(cosine(A,B))
