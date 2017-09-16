
from numpy import *

def gradAscent(data, K):
    dataMat = mat(data)
    print (dataMat)
    m, n = shape(dataMat)
    p = mat(random.random((m, K)))
    q = mat(random.random((K, n)))

    alpha = 0.0002
    beta = 0.02
    maxCycles = 10000

    for step in range(maxCycles):
        for i in range(m):
            for j in range(n):
                if dataMat[i,j] > 0:
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
        if step % 1000 == 0:
            print(loss)

    return p, q


if __name__ == "__main__":
    dataMatrix = [[1, 0, 1, 1, 2], [1, 1 ,0, 2, 2], [0, 0, 1, 3,2],[0, 1, 2,0, 0]]

    p, q = gradAscent(dataMatrix, 3)
    '''
    p = mat(ones((4,10)))
    print p
    q = mat(ones((10,5)))
    '''
    result = p * q
    print (p)
    print (q)

    print(result)