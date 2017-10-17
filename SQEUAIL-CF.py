import functools
from time import sleep

from rec_lib.evaluate import *
from rec_lib.similar import *
from rec_lib.time_inf import SequenceScore, SocialSequenceScore
from rec_lib.trust import KatzCalculator
from rec_lib.utils import *
import os
from pprint import pprint
import multiprocessing


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
if __name__ == '__main__':

    # train_file = 'trainRF-SH-FoursquareCheckins.csv'
    # test_file = 'testRF-SH-FoursquareCheckins.csv'
    loc_center_file = ''
    train_file = 'trainRF-NA-Gowalla_totalCheckins.txt'
    test_file = 'testRF-NA-Gowalla_totalCheckins.txt'

    topns = [100]
    topks = [5,10,15]

    nprs = []
    nres = []
    nvas = []
    print('read_table')
    table = read_checks_table(train_file, split_sig='\t', uin=0, iin=4, timein=1, scorein=None,
                              time_format='%Y-%m-%dT%H:%M:%SZ')
    test = read_checks_table(test_file, split_sig='\t', uin=0, iin=4, timein=1, scorein=None,
                             time_format='%Y-%m-%dT%H:%M:%SZ')
    # table = read_checks_table(train_file, split_sig=',', uin=0, iin=4, timein=3, scorein=None,
    #                           time_format='%Y-%m-%d %H:%M:%S')
    # test = read_checks_table(test_file, split_sig=',', uin=0, iin=4, timein=3, scorein=None,
    #                          time_format='%Y-%m-%d %H:%M:%S')
    root_dir_name = 'mid_data/' + '-'.join(train_file.split('.')[:-1]) + '/'

    # ========= CosineSimilar ================
    sim_fun = CosineSimilar(table)
    sim_fun_name = sim_fun.name

    # ========= CosineSimilar ================
    # sim_fun = JaccardSimilar(table)
    # sim_fun_name = sim_fun.name

    # # ========= SocialSimilar ================
    # friend_dic = read_dic_set('0.1-RF-NA-Gowalla_edges.txt', split_tag='\t')
    # sim_fun = SocialSimilar(friend_dic, default_value=0)
    # sim_fun_name = sim_fun.name


    # # ========= SocialGroupSimilar ================
    # friend_dic = read_dic_set('RF-NA-Gowalla_edges.txt', split_tag='\t')
    # sim_fun = SocialGroupSimilar(friend_dic, 2)
    # sim_fun_name = sim_fun.name

    # ========= trust ===================
    # friend_dic = read_trust_dic('Gowalla_edges.txt')
    # friend_dic = read_dic_set('RF-SH-FoursquareFriendship.csv', split_tag=',')
    # tc = KatzCalculator(friend_dic, max_depth=1, decay=0.5)
    # sim_fun = tc.sim
    # sim_fun_name = tc.name

    # ========== sq_base ================
    #
    # friend_dic = read_dic_set('klndGowalla_edges.txt', split_tag='\t')
    # friend_dic = read_dic_set('RF-SH-FoursquareFriendship.csv', split_tag=',')
    # sim_fun = SequenceScore(table, delta_day=5)
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
        process_num = 4
        users = list(table.keys())
        users_map = [[] for i in range(process_num)]
        for user in table.keys():
            users_map[int(user) % process_num].append(user)
        pool = multiprocessing.Pool(processes=6)
        partial_cal_sim_mat_for_async = functools.partial(cal_sim_mat_for_async, users=users, similar_fun=sim_fun,
                                                          reg_one=True, sort_change=True)

        results = []
        for i in range(process_num):
            results.append(pool.apply_async(partial_cal_sim_mat_for_async, (i, users_map[i],)))
        pool.close()
        pool.join()

        for result in results:
            sim_metrics.update(result.get())
        write_obj(sim_name, sim_metrics)



#13989
    for topn in topns:
        rec_name = dir_name + '-'.join(['rec', str(topn)]) + '.txt'
        ex_rec_name = dir_name + '-'.join(['ex_rec', str(topn)]) + '.txt'
        if os.path.exists(ex_rec_name):
            print('read recommend result from file')
            rec = read_obj(ex_rec_name)
        else:
            print('recommend')
            rec = recommend(table, sim_metrics, topn)
            # write_obj(rec_name, rec)
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

    pprint(nprs)
    pprint(nres)
    pprint(nvas)
