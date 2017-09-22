from rec_lib.evaluate import *
from rec_lib.similar import *
from rec_lib.time_inf import SequenceScore
from rec_lib.trust import TrustCalculator
from rec_lib.utils import *
import os
from pprint import pprint


# 相似度矩阵，
# {
#  u1:[(u2, s12), (u3, s13)}, 
#  u2:[(u1, s21), (u3, s23],
#  u3:[(u1, s31), (u2, s32)]
# }
# topn 邻居数
# recn 推荐数量
def recommend(op_table, friends_dic):
    rec = {}
    for u in op_table:
        rec[u] = {}
        for f in friends_dic[u]:
            for (item, score, time) in op_table[f]:
                if rec[u].keys().__contains__(item):
                    rec[u][item] += 1
                else:
                    rec[u][item] = 1
    for user in rec.keys():
        rec[user] = sort_dict(rec[user])
    # print(rec[0])
    return rec


# 协同过滤主函数
def cf_main(train_file, test_file, topns=None, topks=None):
    if topks is None:
        topks = [20]
    if topns is None:
        topns = [20]
    nprs = []
    nres = []
    nvas = []
    print('read_table')
    table = read_checks_table(train_file, uin=0, iin=4, timein=1, scorein=None)
    test = read_checks_table(test_file, uin=0, iin=4, timein=1, scorein=None)
    root_dir_name = 'mid_data/' + '-'.join(train_file.split('.')[:-1]) + '/'
    friend_dic = read_dic_set('Gowalla_edges.txt')
    dir_name = root_dir_name + 'friend_based' + '/'

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    for topn in topns:
        rec_name = dir_name + '-'.join(['rec', str(topn)]) + '.txt'
        ex_rec_name = dir_name + '-'.join(['ex_rec', str(topn)]) + '.txt'
        if os.path.exists(ex_rec_name):
            print('read recommend result from file')
            rec = read_obj(ex_rec_name)
        else:
            print('recommend')
            rec = recommend(table, friends_dic, topn)
            write_obj(rec_name, rec)
            exclude_dup(table, rec)
            write_obj(ex_rec_name, rec)

        prs = []
        res = []
        vas = []
        for topk in topks:
            print('precision')
            pr = precision(rec, test, topk)
            print(pr)
            re = recall(rec, test, topk)
            print('recall')
            va = variety(rec, topk)

            prs.append(float('%.4f' % pr))
            res.append(float('%.4f' % re))
            vas.append(float('%.4f' % va))
        # print('y1=',prs)
        # print('y2=',res)
        nprs.append(prs.copy())
        nres.append(res.copy())
        nvas.append(vas.copy())

    out_json_to_file(dir_name + 'nprs.txt', nprs)
    out_json_to_file(dir_name + 'nres.txt', nres)
    out_json_to_file(dir_name + 'nvas.txt', nvas)

    return nprs, nres, nvas


if __name__ == '__main__':
    nprs, nres, nvas = cf_main('all-trainklnd-Gowalla_totalCheckins.txt',
                         'all-testklnd-Gowalla_totalCheckins.txt',
                         topns=[5, 10, 15, 20],
                         topks=[1, 2, 3, 5, 7, 10, 15, 20])
    pprint(nprs)
    pprint(nres)
    pprint(nvas)
