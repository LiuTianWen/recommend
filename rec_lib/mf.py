from numpy import *

from rec_lib.similar import cosine
from rec_lib.utils import read_checks_mat


class MyMFModel:
    # def __init__(self, train_file, K):
    #     self.mat, self.uid_no, self.no_uid, self.iid_no, self.no_iid = read_checks_mat(train_file)
    #     self.p, self.q = MyMFModel.gradAscent(self.mat, K)
    #     self.K = K

    def __init__(self, data, K):
        self.p, self.q = MyMFModel.gradAscent(data, K)
        self.uid_no = {k: k for k in range(5)}
        self.iid_no = {k: k for k in range(5)}

    @staticmethod
    def gradAscent(data, K):
        dataMat = mat(data)
        # print (dataMat)
        m, n = shape(dataMat)
        print('shape', m, n)
        p = mat(random.random((m, K)))
        q = mat(random.random((K, n)))

        alpha = 0.002
        beta = 0.01
        maxCycles = 10000

        for step in range(maxCycles):
            print(step)
            for i in range(m):
                for j in range(n):
                    if dataMat[i, j] > 0:
                        #print dataMat[i,j]
                        error = dataMat[i,j]
                        for k in range(K):
                            error = error - p[i,k]*q[k,j]
                        for k in range(K):
                            p[i,k] = p[i,k] + alpha * (2 * error * q[k,j] - beta * p[i,k])
                            q[k,j] = q[k,j] + alpha * (2 * error * p[i,k] - beta * q[k,j])

            loss = 0.0
            for i in range(m):
                for j in range(n):
                    if dataMat[i,j] > 0:
                        error = 0.0
                        for k in range(K):
                            error = error + p[i,k]*q[k,j]
                        loss = (dataMat[i,j] - error) * (dataMat[i,j] - error)
                        for k in range(K):
                            loss = loss + beta * (p[i,k] * p[i,k] + q[k,j] * q[k,j]) / 2

            if loss < 0.001:
                break
            #print step
            # alpha = max(loss/5000, 0.0002)
            # beta = max(alpha * 100, 0.02)
            if step % 1 == 0:
                print(loss)

        return p, q

    def predict(self, u, i):
        return float(self.p[self.uid_no[u], :] * self.q[:, self.iid_no[i]])

    def sim(self, u1, u2):
        return cosine(self.p[self.uid_no[u1]], self.p[self.uid_no[u2]])

if __name__ == "__main__":
    dataMatrix = [[1, 0, 1, 1, 2], [1, 1 ,0, 2, 2], [0, 0, 1, 3, 2],[0, 1, 2,0, 0]]

    mf = MyMFModel(dataMatrix, 3)
    '''
    p = mat(ones((4,10)))
    print p
    q = mat(ones((10,5)))
    '''
    print(mf.p, mf.q)
    print(mf.p * mf.q)