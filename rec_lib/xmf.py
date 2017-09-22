from numpy import *

from rec_lib.similar import cosine
from rec_lib.utils import read_checks_mat, read_checks_table, read_obj, write_obj
import os

class MyMFModel:
    def __init__(self, checks, K, dirname):
        self.checks = checks
        self.K = K
        p_name = dirname + 'p.txt'
        q_name = dirname + 'q.txt'
        if os.path.exists(p_name) and os.path.exists(q_name):
            self.p, self.q = read_obj(p_name), read_obj(q_name)
        else:
            self.p, self.q = MyMFModel.gradAscent(self.checks, K)
            write_obj(p_name, self.p)
            write_obj(q_name, self.q)

    @staticmethod
    def gradAscent(checks, K):
        p = {}
        q = {}
        for u in checks.keys():
            p[u] = random.random(K)
            for check in checks[u]:
                i = check[0]
                if not q.__contains__(i):
                    q[i] = random.random(K)
        alpha = 0.0002
        beta = 0.002
        maxCycles = 2300

        for step in range(maxCycles):
            # print(step)
            for u in p.keys():
                for check in checks[u]:
                    i = check[0]
                    score = check[1]
                    error = score - dot(p[u], q[i])
                    p_delta = alpha * (2 * error * q[i] - beta * p[u])
                    p[u] += p_delta
                    q_delta = alpha * (2 * error * p[u] - beta * q[i])
                    q[i] += q_delta

            loss = 0.0
            for u in p.keys():
                for check in checks[u]:
                    i = check[0]
                    score = check[1]
                    error = dot(p[u], q[i])
                    loss = (score - error) * (score - error)
                    loss += beta * (dot(p[u], p[u]).sum() + dot(q[i], q[i]).sum()) / 2

            if loss < 0.001:
                break

            if step % 10 == 0:
                print(step, loss)

        return p, q

    def predict(self, u, i):
        return float(dot(self.p[u], self.q[i]))

    def sim(self, u1, u2):
        return cosine(self.p[u1], self.p[u2])

if __name__ == "__main__":
    checks = {'0':[(0, 1),(2, 1),(3,1),(4,2)], '1':[(0,1),(1, 1),(3, 2)], '2': [(2, 1), (3, 3), (4, 2)], '3':[(1, 1), (2, 2)]}
    # dataMatrix = [[1, 0, 1, 1, 2], [1, 1 ,0, 2, 2], [0, 0, 1, 3, 2],[0, 1, 2,0, 0]]
    mf = MyMFModel(checks, 2)
    print(mf.q)
    print(mf.p)
    for i in mf.p.keys():
        for j in mf.q.keys():
            print(i, j)
            print(dot(mf.p[i], mf.q[j]))
    '''
    p = mat(ones((4,10)))
    print p
    q = mat(ones((10,5)))
    '''
    # print(mf.predict(0, 1))