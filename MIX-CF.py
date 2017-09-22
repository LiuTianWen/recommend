from rec_lib.evaluate import *
from rec_lib.similar import *
from rec_lib.trust import TrustCalculator
from rec_lib.utils import *
import os
from pprint import pprint
import gc

# 计算相似度矩阵，
# {
#  u1:[(u2, s12), (u3, s13)}, 
#  u2:[(u1, s21), (u3, s23],
#  u3:[(u1, s31), (u2, s32)]
# }
# topn 邻居数
# recn 推荐数量
def recommend(op_table, sim_metrics, topn=None):
    rec = {}
    for u in sim_metrics:
        count = 0
        rec[u] = {}
        for uss in sim_metrics[u]:
            count += 1
            if uss[1] == 0:
                break
            if topn is not None and count >= topn:
                break
            for (item, score, time) in op_table[uss[0]]:
                if rec[u].keys().__contains__(item):
                    rec[u][item] += score * uss[1]
                else:
                    rec[u][item] = score * uss[1]
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
    print('read_table')
    table = read_checks_table(train_file, split_sig=',', uin=0, iin=4, timein=3, scorein=None, time_format='%Y-%m-%d %H:%M:%S')
    test = read_checks_table(test_file, split_sig=',', uin=0, iin=4, timein=3, scorein=None, time_format='%Y-%m-%d %H:%M:%S')
    root_dir_name = 'mid_data/' + '-'.join(train_file.split('.')[:-1]) + '/'

    # ========= MixSimilar ===================
    friends_dic = read_dic_set('FoursquareFriendship.csv', split_tag=',')
    sim_fun_name = 'mix-cos-soc'
    dir_name = root_dir_name + sim_fun_name + '/'
    sim_fun1 = SocialSimilar(friends_dic)
    # sim_fun1 = TrustCalculator(friends_dic, max_depth=3)
    sim_fun2 = CosineSimilar(table)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # cal sim 1
    sim1_name = dir_name + sim_fun1.name
    if os.path.exists(sim1_name):
        print('read sim metrics from file 1')
        sim_metrics1 = read_obj(sim1_name)
        sim_metrics1 = {u: {f[0]: f[1] for f in fs} for u, fs in sim_metrics1.items()}
    else:
        print('cal_sim_mat 1')
        sim_metrics1 = cal_sim_mat(table, similar_fun=sim_fun1, reg_one=False, sort_change=False)
        write_obj(sim1_name, sim_metrics1)

    # call sim 2
    sim2_name = dir_name + sim_fun2.name
    if os.path.exists(sim2_name):
        print('read sim metrics from file 2')
        sim_metrics2 = read_obj(sim2_name)
        sim_metrics2 = {u: {f[0]: f[1] for f in fs} for u, fs in sim_metrics2.items()}
    else:
        print('cal_sim_mat 2')
        sim_metrics2 = cal_sim_mat(table, similar_fun=sim_fun2, reg_one=False, sort_change=False)
        write_obj(sim2_name, sim_metrics2)

    # cal mix sim
    rate = 0
    sim_fun = lambda x, y: rate*sim_metrics1.get(x, {}).get(y, 0) + (1-rate)*sim_metrics2.get(x, {}).get(y, 0)

    dir_name = dir_name + str(rate) + '/'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    sim_name = dir_name + str(rate) + 'M_sim.txt'

    if os.path.exists(sim_name):
        print('read sim metrics from file')
        sim_metrics = read_obj(sim_name)
    else:
        print('cal_sim_mat_mix')
        sim_metrics = cal_sim_mat(table, similar_fun=sim_fun)
        write_obj(sim_name, sim_metrics)

    del sim_metrics1
    del sim_metrics2
    gc.collect()

    for topn in topns:
        rec_name = dir_name + '-'.join(['rec', str(topn)]) + '.txt'
        ex_rec_name = dir_name + '-'.join(['ex_rec', str(topn)]) + '.txt'
        if os.path.exists(ex_rec_name):
            print('read recommend result from file')
            rec = read_obj(ex_rec_name)
        else:
            print('recommend')
            rec = recommend(table, sim_metrics, topn)
            write_obj(rec_name, rec)
            exclude_dup(table, rec)
            write_obj(ex_rec_name, rec)

        prs = []
        res = []
        for topk in topks:
            print('precision')
            pr = precision(rec, test, topk)
            print(pr)
            re = recall(rec, test, topk)
            print('recall')
            prs.append(float('%.4f' % pr))
            res.append(float('%.4f' % re))
        # print('y1=',prs)
        # print('y2=',res)
        nprs.append(prs.copy())
        nres.append(res.copy())

    out_json_to_file(dir_name + 'nprs.txt', nprs)
    out_json_to_file(dir_name + 'nres.txt', nres)

    return nprs, nres


if __name__ == '__main__':
    nprs, nres = cf_main('trainna-FoursquareCheckins.csv',
                         'testna-FoursquareCheckins.csv',
                         topns=[5, 10, 15, 20],
                         topks=[1, 2, 3, 5, 7, 10, 15, 20])
    pprint(nprs)
    pprint(nres)
