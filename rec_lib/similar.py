import numpy as np
import time
from numpy import *
from numpy import array
from collections import Counter
from rec_lib.utils import read_obj, dic_value_reg_one, sort_dict
import gc


class CosineSimilar:
    name = 'cosine_1'

    def __init__(self, table, limit=1):
        self.table = table
        self.limit = limit

    def __call__(self, u1, u2):
        x = self.table[u1]
        y = self.table[u2]
        mx = Counter([e[0] for e in x])
        my = Counter([e[0] for e in y])
        if self.limit is not None:
            for k, v in mx.items():
                if v > self.limit:
                    mx[k] = self.limit
            for k, v in my.items():
                if v > self.limit:
                    my[k] = self.limit
        downx = sum([v*v for k, v in mx.items()])
        downy = sum([v*v for k, v in my.items()])
        up = sum([mx[k] * my[k] for k in set(mx.keys()) & set(my.keys())])
        # print(up)
        return math.sqrt(up * up / (downx * downy))


class SocialSimilar:
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


class SocialAndCosineMixSimilar:
    name = 'soc_loc'

    def __init__(self, friends_dic, table, rate=0.5):
        self.friend_similar = SocialSimilar(friends_dic)
        self.cosine_similar = CosineSimilar(table)
        self.rate = rate

    def __call__(self, u1, u2):
        fs = self.friend_similar(u1, u2)
        cs = self.cosine_similar(u1, u2)
        return self.rate * fs + (1 - self.rate) * cs



# for array
def cosine(A, B):
    # noinspection PyBroadException
    try:
        num = float(np.dot(A, B.T))  # 若为行向量则 A * B.T
        denom = linalg.norm(A) * linalg.norm(B)
        cos = num / denom  # 余弦值
        sim = 0.5 + 0.5 * cos  # 归一化
    except:
        print(A, len(A), len(A[0]), type(A))
        print(B, len(B), len(B[0]), type(B))
        return 0
    return sim


# for dic
def cosine_for_dic(dx, dy):
    down1 = sum([v * v for v in dx.values()])
    down2 = sum([v * v for v in dy.values()])
    up = 0
    for k in dx.keys():
        up += dx.get(k, 0) * dy.get(k, 0)
    return up / math.sqrt(down1 * down2)


# async
def cal_sim_mat_for_async(worknum, user_queue, users, similar_fun, reg_one=True, sort_change=True):
    sim_mat = {}
    print('run thread' + str(worknum))
    count = 0
    while user_queue:
        count += 1

        user = user_queue.pop()

        print(len(user_queue), worknum)
        if user is not None:
            sim_mat[user] = {}
            for u in users:
                if u == user:
                    continue
                s = similar_fun(user, u)
                if s > 0:
                    sim_mat[user][u] = s
            if reg_one:
                dic_value_reg_one(sim_mat[user])
            if sort_change:
                sim_mat[user] = sort_dict(sim_mat[user])
            # if count % 20 == 0:
            #     gc.collect()
    return sim_mat


# static fun
def cal_sim_mat(table, similar_fun, reg_one=True, sort_change=True):
    count = 0
    ids = list(table.keys())
    total = len(ids) * len(ids)
    l = len(ids)
    print(l)
    TM = {}
    for u1 in ids:
        if not TM.__contains__(u1):
            TM[u1] = {}
        for u2 in ids:
            if u1 == u2:
                continue
            else:
                count += 1
                if count % 10000 == 0:
                    print(count, total)
                s = similar_fun(u2, u1)
                if s > 0 :
                    TM[u1][u2] = s
        if TM[u1] is None:
            print(u1, TM[u1])
        if reg_one:
            dic_value_reg_one(TM[u1])

    if sort_change:
        TM = {k: sort_dict(v) for k, v in TM.items()}

    return TM


if __name__ == '__main__':
    A = array([[1, 2, 3]])
    B = array([[1, 2, 3]])
    print(cosine(A, B))
