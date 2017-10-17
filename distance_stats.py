import matplotlib.pyplot as plt
import numpy as np

from center import read_user_center
from rec_lib.geo_distance import *
from rec_lib.utils import *


# 统计距离数量
def dis_stats(filename, user_center, split_sig=',', uin=0, lain=1, loin=2):
    # log(1/421161)
    table = {}
    cs = float(1)
    with open(filename) as f:
        for each in f:

            elements = each.strip().split(split_sig)
            u = elements[uin]
            la = float(elements[lain])
            lo = float(elements[loin])
            dis = haversine(lo, la, float(user_center.get(u)[1]), float(user_center.get(u)[0]))
            dp = int(dis)+1
            
            if dp > 100:
                continue
            cs += 1
            if table.__contains__(dp):
                table[dp] += 1
            else:
                table[dp] = 1

    table = [[k, v/cs] for k, v in table.items()]
    return table


def dis_stats_no_center(filename, split_sig=',', uin=0, iin=4, lain=1, loin=2):
    checks = {}
    table = {}
    cs = float(1)
    with open(filename) as f:
        for each in f:
            try:
                elements = each.strip().split(split_sig)
                u = elements[uin]
                i = elements[iin]
                la = float(elements[lain])
                lo = float(elements[loin])
                if checks.get(u) is not None:
                    checks[u][i] = (la, lo)
                else:
                    checks[u] = {i: (la, lo)}
            except Exception as e:
                print(split_sig)
                print(elements)
                raise e

    for u, uchecks in checks.items():
        for i in uchecks.keys():
            for j in uchecks.keys():
                dis = haversine(uchecks[j][0], uchecks[j][1], uchecks[i][0], uchecks[i][1])
                dp = int(dis) + 1
                # if dp > 1000:
                #     continue
                cs += 1
                if table.__contains__(dp):
                    table[dp] += 1
                else:
                    table[dp] = 1

    table = [[k, v/cs] for k, v in table.items()]
    return table


def linefit(x, y):

    N = float(len(x))
    sx, sy, sxx, syy, sxy = 0, 0, 0, 0, 0
    for i in range(0, int(N)):
        sx += x[i]
        # print(i, sx, x[i], y[i])
        sy += y[i]
        sxx += x[i] * x[i]
        syy += y[i] * y[i]
        sxy += x[i] * y[i]
    a = (sy * sx / N - sxy) / (sx * sx / N - sxx)
    b = (sy - a * sx) / N
    r = abs(sy * sx / N - sxy) / math.sqrt((sxx - sx * sx / N) * (syy - sy * sy / N))
    return a, b, r


if __name__ == '__main__':
    # center_file = 'trainna-FoursquareUserCenter.csv'
    # check_file = 'trainna-FoursquareCheckins.csv'

    # center_file = 'all-trainklnd-Gowalla_UserCenter.txt'
    # check_file = 'all-trainklnd-Gowalla_totalCheckins.txt'

    # center_file = '../na-Gowalla_UserCenter.txt'
    # check_file = '../na-Gowalla_totalCheckins.txt'

    # check_file = 'trainRF-SH-FoursquareCheckins.csv'
    # center_file = 'trainRF-SH-FoursquareUserCenter.csv'
    check_file = 'trainRF-NA-Gowalla_totalCheckins.txt'
    center_file = 'trainRF-NA-Gowalla_UserCenter.txt'
    user_center = read_user_center(center_file)
    table = dis_stats(check_file, user_center, split_sig='\t', lain=2, loin=3)
    # table = dis_stats_no_center(check_file, split_sig=',', lain=1, loin=2)
    stats = mat(table).T
    # log_stats = mat([[k, v] for k, v in log_table.items()]).T
    # plt.title('distance check distribution of Foursquare')
    logx = log10(stats[0]).getA()[0]
    logy = log10(stats[1]).getA()[0]
    fig = plt.figure()
    ax1 = fig.add_subplot('121')
    ax2 = fig.add_subplot('122')
    ax1.set_ylabel('check probability')
    ax1.set_xlabel('check distance: /km')
    ax2.set_ylabel('log(check probability)')
    ax2.set_xlabel('log(check distance)')

    ax1.scatter(stats[0], stats[1], label='origin data')
    ax2.scatter(logx, logy, label='origin data')

    z1 = np.polyfit(logx, logy, 1)  # 一次多项式拟合，相当于线性拟合
    p1 = np.poly1d(z1)
    a = z1[0]
    b = z1[1]

    print(p1)
    x = np.linspace(0, 2.5, 100)
    y = a * x + b
    print('A',pow(10, b))
    print('B', a)
    ax2.plot(x, y, label='$y=-1.616x-0.073')
    X = np.linspace(1, 50, 100)
    Y = pow(10, b) * pow(X, a)
    ax1.plot(X, Y, label='$y=0.845^{-1.617}$')

    ax1.legend(loc='upper right')
    ax2.legend(loc='upper right')

    ax1.set_title('Gowalla checks probability')
    ax2.set_title('Gowalla power law distribution: log')
    # ax1.set_title('Foursqaure checks probability')
    # ax2.set_title('Foursqaure power law distribution: log')
    plt.show()


    # Foursquare-na : -0.9911 x - 3.032
    # gowalla-na : -1.171 x - 1.924
    # Foursquare-RF: A 0.434021925139 B -1.31013019716