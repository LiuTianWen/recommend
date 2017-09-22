import functools

import numpy as np


def sigmoid_influence(x, a, b):
    if x < 0:
        return 0
    else:
        return 1 - (1 / (1 + np.exp(-(b * x - a * b))))

def day_inf(a, b):
    if a.__ge__(b):
        d = (a - b).days
        return d if 1/(d+1) < 3 else 0
    else:
        return 0

class SequenceSimilar:
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
                        print(count / total)
                    TM[u1].append((u2, similar_fun(u2, u1)))

            sum_score = sum([e[1] for e in TM[u1]])
            if sum_score > 0:
                TM[u1] = [[e[0], e[1] / sum_score] for e in TM[u1]]
        self.TM = TM

    def __call__(self, u1, u2):
        # noinspection PyBroadException
        try:
            if self.friends_dic[u1].__contains__(u2):
                return self.TM[u1][u2]
            else:
                return 0
        except:
            return 0


# how many times u1 followed u2
# delta: time_limit
class SequenceScore:
    def __init__(self, table, delta=24 * 60 * 60):
        self.table = table
        self.delta = delta
        # self.one_day_influence = functools.partial(sigmoid_influence, a=delta/(60*60), b=2)
    @property
    def name(self):
        return 'sq_score' + '3d'# + str(self.delta)

    def __call__(self, u1, u2):
        x = self.table[u1]
        y = self.table[u2]
        mx = {}
        for e in x:
            if not mx.__contains__(e[0]):
                mx[e[0]] = [e[2], 1]
            else:
                mx[e[0]][1] += 1
                if mx[e[0]][0] > e[2]:
                    mx[e[0]][0] = e[2]
        my = {}
        for e in y:
            if not my.__contains__(e[0]):
                my[e[0]] = [e[2], 1]
            else:
                my[e[0]][1] += 1
                if my[e[0]][0] > e[2]:
                    my[e[0]][0] = e[2]
        up = 0
        for k, v in mx.items():
            # if my.get(k) and v[0].__ge__(my[k][0]) and 0 <= (v[0] - my[k][0]).seconds < self.delta:
            #     up += 1
            if my.get(k):
                # up += self.one_day_influence((v[0] - my[k][0]).seconds/(60*60))
                up += day_inf(v[0], my[k][0])
        return up / len(mx)
