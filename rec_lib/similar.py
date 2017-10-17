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

class JaccardSimilar:
    name = 'Jaccard'

    def __init__(self, table, limit=1):
        self.table = table
        self.limit = limit

    def __call__(self, u1, u2):
        x = self.table[u1]
        y = self.table[u2]
        mx = set([e[0] for e in x])
        my = set([e[0] for e in y])
        up = len(mx & my)
        down = len(mx | my)
        return up/down


class SocialSimilar:

    @property
    def name(self):
        return 'soc' + str(self.default_value)

    def __init__(self, friends_dic, default_value=0.5): # 目前来看，这个0.5效果最好
        self.friends_dic = friends_dic
        self.default_value = default_value

    def __call__(self, u1, u2):
        up = len(set(self.friends_dic.get(u1, set())) & self.friends_dic.get(u2, set()))
        down = len(self.friends_dic.get(u1, set()) | self.friends_dic.get(u2, set()))
        if self.friends_dic.get(u1, set()).__contains__(u2):
            default_value = self.default_value
        else:
            default_value = 0
        if down:
            return (1 - self.default_value) * (up / down) + default_value
        else:
            return default_value


class SocialGroupSimilar:

    @property
    def name(self):
        return 'soc-group'+str(self.depth)

    def __init__(self, friend_dic, depth=2): # 目前来看，这个0.5效果最好
        self.friend_dic = friend_dic
        self.depth = depth
        self.friends_dic_in_n = self.extense_friends()
        self.sim_mat = {}
        # self.cal_sim_m()

    def extense_friends(self):
        print('calulate group friend')
        nfd = {}
        if self.depth == 1:
            return self.friend_dic
        for u in self.friend_dic.keys():
            # print(u)
            f = self.friend_dic.get(u, set()).copy()
            f.add(u)
            t = f.copy()
            for i in range(1, self.depth):
                nt = set()
                for e in t:
                    nt.update(self.friend_dic.get(e, set()))
                t = nt - f
                f.update(nt)
            f.remove(u)
            nfd[u] = {int(e) for e in f}
        return nfd

    def cal_sim_m(self):
        for u1 in self.friend_dic.keys():
            for u2 in self.friend_dic.keys():
                if u1 == u2 or self.sim_mat.__contains__(u1) and self.sim_mat[u1].__contains__(u2):
                    continue
                if not self.sim_mat.__contains__(u1):
                    self.sim_mat[u1] = {}
                if not self.sim_mat.__contains__(u2):
                    self.sim_mat[u2] = {}
                up = self.friends_dic_in_n.get(u1, set()) & self.friends_dic_in_n.get(u2, set())
                down = self.friends_dic_in_n.get(u1, set()) | self.friends_dic_in_n.get(u2, set())
                self.sim_mat[u1][u2] = len(up)/len(down)
                self.sim_mat[u2][u1] = len(up)/len(down)

    def __call__(self, u1, u2):
        try:
            if self.depth == 0:
                return 1 if self.friend_dic.get(u1, set()).__contains__(u2) else 0

            if not self.sim_mat.__contains__(u1) or not self.sim_mat[u1].__contains__(u2):
                if not self.sim_mat.__contains__(u1):
                    self.sim_mat[u1] = {}
                if not self.sim_mat.__contains__(u2):
                    self.sim_mat[u2] = {}
                up = len(self.friends_dic_in_n.get(u1, set()) & self.friends_dic_in_n.get(u2, set()))
                down = len(self.friends_dic_in_n.get(u1, set()) | self.friends_dic_in_n.get(u2, set()))
                if down == 0:
                    down == 1
                self.sim_mat[u1][u2] = up / down
                self.sim_mat[u2][u1] = up / down

            return self.sim_mat[u1][u2]
        except:
            return 0

    # def

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
                # if count % 10000 == 0:
                #     print(count, total)
                s = similar_fun(u1, u2)
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
