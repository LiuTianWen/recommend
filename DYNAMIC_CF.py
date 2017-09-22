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


def recommend_for_user(op_table, user, sim_list, topns):
    sim_list = sort_dict(sim_list)
    max_top = max(topns)
    recs = {k: None for k in topns}
    rec = {}
    count = 0
    for uss in sim_list:
        count += 1
        if uss[1] == 0 or count > max_top:
            break
        for (item, score, time) in op_table[uss[0]]:
            if rec.keys().__contains__(item):
                rec[item] += score * uss[1]
            else:
                rec[item] = score * uss[1]
        if recs.__contains__(count):
            recs[count] = sort_dict(rec)
    if count <= max_top:
        for k in recs.keys():
            if k >= count:
                recs[k] = rec
    old_items = set([i[0] for i in op_table.get(user, [])])
    for k, rec in recs.items():
        recs[k] = [e for e in recs[k] if not old_items.__contains__(e[0])]
    return recs

def worker(lock, targets, table, name, recall_name, precision_name, sim_fun1, sim_fun2, rate, topns):
    print('run Thread:', name, len(targets))
    limit = 3000
    count = 0
    for target in targets:
        count += 1
        # print('thread'+str(name)+' select neighbors for target', target, datetime.now())
        sim_list = {}
        for u in table.keys():
            if u == target:
                continue
            # s1 = sim_fun1(target, u)
            s2 = sim_fun2(target, u)
            # s = rate*s1 + (1-rate)*s2
            if s2 > 0:
                sim_list[u] = s2
        # print('rec for target', datetime.now())
        # print('run sim:', name)
        recs = recommend_for_user(table, target, sim_list, topns)
        # pprint(recs)
        # print('evaluate', datetime.now())
        with lock:
            d_recall = read_obj(recall_name)
            d_precision = read_obj(precision_name)
            d_recall.add_recs(target, recs)
            d_precision.add_recs(target, recs)
            write_obj(recall_name, d_recall)
            write_obj(precision_name, d_precision)
        # print(name, 'write')
        if count % 10 == 0:
            print('thread:' + str(name))
            print('recall',d_recall.get_result())
            print('precision',d_precision.get_result())
        if count > limit:
            print('over')
            break

# 协同过滤主函数
if __name__ == '__main__':

    train_file = 'trainFoursquareCheckins.csv'
    test_file = 'testFoursquareCheckins.csv'
    topns = [5, 10, 15, 20]
    topks = [1, 5]

    print('read_table')
    table = read_checks_table(train_file, split_sig=',', uin=0, iin=4, timein=3, scorein=None, time_format='%Y-%m-%d %H:%M:%S')
    test = read_checks_table(test_file, split_sig=',', uin=0, iin=4, timein=3, scorein=None, time_format='%Y-%m-%d %H:%M:%S')
    root_dir_name = 'mid_data/' + '-'.join(train_file.split('.')[:-1]) + '/'


    # ========= MixSimilar ===================
    friends_dic = read_dic_set('FoursquareFriendship.csv', split_tag=',')
    sim_fun1 = None #SocialSimilar(friends_dic)
    # sim_fun1 = TrustCalculator(friends_dic, max_depth=3)
    sim_fun2 = CosineSimilar(table)
    sim_fun_name = sim_fun2.name
    dir_name = root_dir_name + sim_fun_name + '/'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    rate = 0.1

    recall_name = dir_name + 'recall'
    precision_name = dir_name + 'precision'
    d_recall = D_Recall(test_table=test, topks=topks, topns=topns)
    d_precision = D_Precision(test_table=test, topks=topks, topns=topns)

    write_obj(recall_name, d_recall)
    write_obj(precision_name, d_precision)

    import multiprocessing

    pool_size = 6
    pool = multiprocessing.Pool(processes=pool_size)
    lock = multiprocessing.Manager().Lock()
    target_map = [[] for i in range(pool_size)]
    for u in table.keys():
        target_map[int(u)%pool_size].append(u)
    for i in range(pool_size):
        pool.apply_async(func=worker, args=(lock, target_map[i], table, i, recall_name, precision_name, sim_fun1, sim_fun2, rate, topns))
    pool.close()
    pool.join()
    d_recall = read_obj(recall_name)
    d_precision = read_obj(precision_name)
    print('d_recall', d_recall.get_result())
    print('d_precision', d_precision.get_result())