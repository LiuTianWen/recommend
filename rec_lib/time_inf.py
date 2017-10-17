import functools

import numpy as np

from rec_lib.similar import cosine_for_dic


def sigmoid_influence(x, a, b):
    if x < 0:
        return 0
    else:
        return 1 - (1 / (1 + np.exp(-(b * x - a * b))))


def day_inf(a, b, delta_day=1):
    if a.__ge__(b):
        d = (a - b).days
        # return 1 if d <= delta_day else 0
        return 1 / (d + 1) if d <= delta_day else 0
    else:
        return 0

# how many times u1 followed u2
# delta: time_limit
class SequenceScore:
    def __init__(self, table, delta_day=1):
        self.table = table
        self.delta_day = delta_day

    @property
    def name(self):
        return 'sq_score' + str(self.delta_day) + 'd'

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
                up += day_inf(v[0], my[k][0], self.delta_day)
        return up / len(mx)


class SocialSequenceScore:
    def __init__(self, table, friend_dic, delta_day=1, default_value=0.5):
        self.table = table
        self.delta_day = delta_day
        self.time_inf = {}
        self.reverse_time_inf = {}
        self.friend_dic = friend_dic
        self.default_value = default_value
        for u1 in self.friend_dic.keys():
            print(u1)
            max_inf = 0
            for u2 in self.friend_dic.get(u1):
                if u1 != u2:
                    if not self.time_inf.__contains__(u1):
                        self.time_inf[u1] = {}
                    if not self.reverse_time_inf.__contains__(u2):
                        self.reverse_time_inf[u2] = {}
                    inf = self.time_score(u1, u2)
                    if inf > max_inf:
                        max_inf = inf
                    self.time_inf[u1][u2] = inf
                    self.reverse_time_inf[u2][u1] = inf
            if max_inf > 0:
                for u2 in self.friend_dic.get(u1):
                    self.time_inf[u1][u2] /= max_inf
                    self.reverse_time_inf[u2][u1] /= max_inf

    @property
    def name(self):
        return 'soc_time_inf' + str(self.delta_day) + 'd'

    def time_score(self, u1, u2):
        if self.time_inf.get(u1,{}).get(u2):
            return self.time_inf[u1][u2]
        x = self.table.get(u1, {})
        y = self.table.get(u2, {})
        mx = {}
        for e in x:
            if not mx.__contains__(e[0]):
                mx[e[0]] = [e[2], 1]
            else:
                mx[e[0]][1] += 1
                if mx[e[0]][0] > e[2]:
                    mx[e[0]][0] = e[2]
        if not mx:
            return 0
        my = {}
        for e in y:
            if not my.__contains__(e[0]):
                my[e[0]] = [e[2], 1]
            else:
                my[e[0]][1] += 1
                if my[e[0]][0] > e[2]:
                    my[e[0]][0] = e[2]
        if not my:
            return 0
        up = 0
        for k, v in mx.items():
            # if my.get(k) and v[0].__ge__(my[k][0]) and 0 <= (v[0] - my[k][0]).seconds < self.delta:
            #     up += 1
            if my.get(k):
                # up += self.one_day_influence((v[0] - my[k][0]).seconds/(60*60))
                up += day_inf(v[0], my[k][0])
        self.time_inf[u1][u2] = up
        return self.time_inf[u1][u2]

    def __call__(self, u1, u2):
        up = 0
        down = 0
        for mid_f, rinf in self.reverse_time_inf.get(u2).items():
            if self.time_inf.get(u1, {}).__contains__(u1):
                up += self.time_inf[u1][mid_f] * self.time_inf[mid_f][u2]
                down += self.time_inf[u1][mid_f]
        return self.default_value if self.friend_dic.__contains__(u2) else 0 + (1 - self.default_value) * (up/down)
