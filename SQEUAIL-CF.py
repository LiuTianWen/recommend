import functools
from time import sleep

from rec_lib.evaluate import *
from rec_lib.similar import *
from rec_lib.time_inf import SequenceScore
from rec_lib.trust import TrustCalculator
from rec_lib.utils import *
import os
from pprint import pprint
import multiprocessing


# 相似度矩阵，
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
        # neihbor_rank = sort_dict(sim_metrics[u])
        neighbor_rank = sim_metrics.get(u)
        for uss in neighbor_rank:
            count += 1
            if uss[1] == 0:
                break
            if topn is not None and count >= topn:
                break
            item_set = {item: score for (item, score, time) in op_table[uss[0]]}
            for item, score in item_set.items():
                if rec[u].keys().__contains__(item):
                    rec[u][item] += score * uss[1]
                else:
                    rec[u][item] = score * uss[1]
    for user in rec.keys():
        rec[user] = sort_dict(rec[user])
    # print(rec[0])
    return rec


def async_test(thread_name, sim_mat, lock):
    for i in range(10):
        with lock:
            print(str(thread_name) + ':' + str(i))
            sim_mat[str(thread_name) + ':' + str(i)] = i
            sleep(0.5)

# 协同过滤主函数
if __name__ == '__main__':

    train_file = 'trainna-FoursquareCheckins.csv'
    test_file = 'testna-FoursquareCheckins.csv'
    topns = [5, 10, 15, 20]
    topks = [1, 2, 3, 5, 7, 10, 15, 20]

    nprs = []
    nres = []
    nvas = []
    print('read_table')
    table = read_checks_table(train_file, split_sig=',', uin=0, iin=4, timein=3, scorein=None, time_format='%Y-%m-%d %H:%M:%S')
    test = read_checks_table(test_file, split_sig=',', uin=0, iin=4, timein=3, scorein=None, time_format='%Y-%m-%d %H:%M:%S')
    root_dir_name = 'mid_data/' + '-'.join(train_file.split('.')[:-1]) + '/'

    # ========= CosineSimilar ================
    sim_fun = CosineSimilar(table)
    sim_fun_name = sim_fun.name

    # # ========= SocialSimilar ================
    # friend_dic = read_dic_set('FoursquareFriendship.csv', split_tag=',')
    # sim_fun = SocialSimilar(friend_dic)
    # sim_fun_name = sim_fun.name

    # ========= trust ===================
    # friend_dic = read_trust_dic('Gowalla_edges.txt')
    # tc = TrustCalculator(friend_dic, max_depth=3, decay=0.8)
    # sim_fun = lambda x, y: tc.sim(x, y)
    # sim_fun_name = tc.name

    # ========== sq_base ================
    # sim_fun = SequenceScore(table, delta=26*60*60)
    # sim_fun_name = sim_fun.name

    dir_name = root_dir_name + sim_fun_name + '/'
    sim_name = dir_name + 'S_sim.txt'

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    if os.path.exists(sim_name):
        print('read sim metrics from file')
        sim_metrics = read_obj(sim_name)
    else:
        print('cal_sim_mat')
        sim_metrics = {}
        process_num = 6
        users = list(table.keys())
        users_map = [[] for i in range(process_num)]
        for user in table.keys():
            users_map[int(user) % 6].append(user)
        pool = multiprocessing.Pool(processes=process_num)
        partial_cal_sim_mat_for_async = functools.partial(cal_sim_mat_for_async, users=users, similar_fun=sim_fun, reg_one=False, sort_change=True)
        # partial_test = functools.partial(async_test)
        # print(users_map[0])
        # partial_cal_sim_mat_for_async(0, users_map[0])
        results = []
        for i in range(6):
            results.append(pool.apply_async(partial_cal_sim_mat_for_async, (i, users_map[i], )))
        pool.close()
        pool.join()

        for result in results:
            sim_metrics.update(result.get())
        write_obj(sim_name, sim_metrics)

    out_json_to_file('out_file.txt', sim_metrics)

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
    out_json_to_file(dir_name + 'sim.json', sim_metrics)

    pprint(nprs)
    pprint(nres)
    pprint(nvas)

