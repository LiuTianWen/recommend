from rec_lib.evaluate import *
from rec_lib.sim_mix import keys_to_index, dic_to_mat
from rec_lib.similar import *
# from rec_lib.trust import TrustCalculator
from rec_lib.time_inf import SequenceScore, SocialSequenceScore
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
            item_set = {item: score for (item, score, time, la, lo) in op_table[uss[0]]}
            for item, score in item_set.items():
                if rec[u].keys().__contains__(item):
                    rec[u][item] += score * uss[1]
                else:
                    rec[u][item] = score * uss[1]
    for user in rec.keys():
        rec[user] = sort_dict(rec[user])
    # print(rec[0])
    return rec


# 协同过滤主函数
def cf_main(train_file, test_file, friend_file, ratess, topns=None, topks=None):
    if topks is None:
        topks = [20]
    if topns is None:
        topns = [20]

    print('read_table')
    try:
        table = read_checks_table(train_file, split_sig=',', uin=0, iin=4, timein=3, scorein=None, time_format='%Y-%m-%d %H:%M:%S')
        test = read_checks_table(test_file, split_sig=',', uin=0, iin=4, timein=3, scorein=None, time_format='%Y-%m-%d %H:%M:%S')
    except :
        table = read_checks_table(train_file, split_sig='\t', uin=0, iin=4, timein=1, scorein=None,
                                  time_format='%Y-%m-%dT%H:%M:%SZ')
        test = read_checks_table(test_file, split_sig='\t', uin=0, iin=4, timein=1, scorein=None,
                                 time_format='%Y-%m-%dT%H:%M:%SZ')

    root_dir_name = 'mid_data/' + '-'.join(train_file.split('.')[:-1]) + '/'

    # ========= MixSimilar ===================
    try:
        friends_dic = read_dic_set(friend_file, split_tag=',')
    except:
        friends_dic = read_dic_set(friend_file, split_tag='\t')

    # sim_fun1 = SocialSimilar(friends_dic, 0.5)
    # sim_fun1 = TrustCalculator(friends_dic, max_depth=3)
    # sim_fun2 = JaccardSimilar(table)
    # sim_fun1 = CosineSimilar(table)
    # sim_fun2 = SequenceScore(table)

    # sim_funs = [
    #     SocialSimilar(friends_dic, 0.5),
    #     SequenceScore(table, delta_day=1),
    #     CosineSimilar(table)
    # ]

    # sim_funs = [
    #     SocialSimilar(friends_dic, 0),
    #     JaccardSimilar(table)
    # ]

    sim_funs = [
        SocialGroupSimilar(friends_dic, 0),
        SocialGroupSimilar(friends_dic, 1),
        SocialGroupSimilar(friends_dic, 2)
    ]

    sim_fun_name = '-'.join([sim_m.name for sim_m in sim_funs])
    # sim_fun_name = 'soc-m-d'
    root_dir_name = root_dir_name + sim_fun_name + '/'

    sim_metricss=[]

    if not os.path.exists(root_dir_name):
        os.makedirs(root_dir_name)


    ulist = list(table.keys())
    index = keys_to_index(ulist)

    for i in range(len(sim_funs)):
        sim_fun = sim_funs[i]

        sim_name = root_dir_name + sim_fun.name
        if os.path.exists(sim_name):
            print('read sim metrics from file ' + str(i))
            sim_metrics = read_obj(sim_name)
            if isinstance(sim_metrics.get('685'), list):
                sim_metrics = {u: {f[0]: f[1] for f in fs} for u, fs in sim_metrics.items()}
        else:
            print('cal_sim_mat:' + str(i))
            sim_metrics = cal_sim_mat(table, similar_fun=sim_fun, reg_one=True, sort_change=False)
            write_obj(sim_name, sim_metrics)
        sim_metrics = dic_to_mat(index, sim_metrics)
        sim_metricss.append(sim_metrics)

    for rates in ratess:
        nprs = []
        nres = []
        # cal mix sim
        mix_mat = np.zeros(shape=(len(ulist), len(ulist)))
        for i in range(len(rates)):
            mix_mat = mix_mat + rates[i] * sim_metricss[i]
        sim_fun = lambda x, y: mix_mat[index[x], index[y]]

        dir_name = root_dir_name + str(rates) + '/'
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        else:
            continue

        for topn in topns:
            # rec_name = dir_name + '-'.join(['rec', str(topn)]) + '.txt'
            ex_rec_name = dir_name + '-'.join(['ex_rec', str(topn)]) + '.txt'
            if os.path.exists(ex_rec_name):
                print('read recommend result from file')
                rec = read_obj(ex_rec_name)
            else:

                # 没有推荐残留的话，重新计算相似度再计算
                sim_name = dir_name + str(rates) + 'mix.sim'
                if os.path.exists(sim_name):
                    print('read sim metrics from file')
                    mix_sim_metrics = read_obj(sim_name)
                else:
                    print('cal_sim_mat_mix')
                    mix_sim_metrics = cal_sim_mat(table, similar_fun=sim_fun)
                    # write_obj(sim_name, mix_sim_metrics)

                print('recommend')
                rec = recommend(table, mix_sim_metrics, topn)
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
            nprs.append(prs.copy())
            nres.append(res.copy())

        out_json_to_file(dir_name + 'nprs.txt', nprs)
        out_json_to_file(dir_name + 'nres.txt', nres)


if __name__ == '__main__':

    train_file = 'trainRF-NA-Gowalla_totalCheckins.txt'
    test_file = 'testRF-NA-Gowalla_totalCheckins.txt'
    friend_file = '0.1-RF-NA-Gowalla_edges.txt'
    # train_file = 'train-corolado-Gowalla_totalCheckins.txt'
    # test_file = 'test-corolado-Gowalla_totalCheckins.txt'
    # friend_file = 'klndGowalla_edges.txt'

    ratess = []
    for x in np.arange(0, 11, 1):
        for y in np.arange(0, 11-x, 1):
            ratess.append([float("%.2f" % (x/10)),float("%.2f" % (y/10)),float("%.2f" % ((10-x-y)/10))])
    # for x in np.arange(0, 11, 1):
    #     ratess.append([float("%.2f" % (x / 10)), float("%.2f" % ((10 - x) / 10))])
    ratess= [[0.3, 0.5, 0.2]]
    # ratess = [[0.1, 0.9], [0.5, 0.5]]

    pprint(ratess)

    cf_main(train_file,
            test_file,
            friend_file,
            ratess,
            topns=[5, 10],
            topks=[5, 10],
            )

