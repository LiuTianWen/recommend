# -*- coding:utf-8 -*-
import os
from math import log

from rec_lib.utils import read_checks_table, dic_value_reg_one, read_obj, write_obj, sort_dict, read_dic_set, exclude_dup
from rec_lib.similar import cosine_for_dic, cal_sim_mat
from rec_lib.evaluate import *
from random import random
from pprint import pprint


class MyLDA:
    def __init__(self, train_filename, topic_num, read_from_file=False):
        self.train_filename = train_filename
        self.topic_num = topic_num
        self.checks = read_checks_table(train_filename)

        dir_name = 'mid_data/' + '-'.join(train_filename.split('.')[:-1]) + '/lda' + str(topic_num) + 't/'
        u_in_z_filename = dir_name + 'pr_u_in_z.txt'
        i_in_z_filename = dir_name + 'pr_i_in_z.txt'
        z_filename = dir_name + 'pz.txt'
        pr_filename = dir_name + 'pr.txt'
        z_in_u_filename = dir_name + 'pr_z_in_u.txt'

        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        if os.path.exists(u_in_z_filename) and os.path.exists(i_in_z_filename) and os.path.exists(z_filename) and os.path.exists(pr_filename) and os.path.exists(z_in_u_filename):
            self.pr_u_in_z, self.pr_i_in_z, self.pz, self.pr, self.pr_z_in_u = read_obj(u_in_z_filename), read_obj(i_in_z_filename), read_obj(z_filename), read_obj(pr_filename), read_obj(z_in_u_filename)
        else:
            self.pr_u_in_z, self.pr_i_in_z, self.pz, self.pr = MyLDA.init_data(topic_num, self.checks)
            MyLDA.em_loop(self.pr_u_in_z, self.pr_i_in_z, self.pz, self.pr, self.checks)
            self.pr_z_in_u = {}
            for u in self.checks.keys():
                self.pr_z_in_u[u] = {}
                for z in self.pz.keys():
                    self.pr_z_in_u[u][z] = 0
                    for check in self.checks[u]:
                        i = check[0]
                        self.pr_z_in_u[u][z] += self.pr[(u, i)][z]
                dic_value_reg_one(self.pr_z_in_u[u])
            write_obj(u_in_z_filename, self.pr_u_in_z)
            write_obj(i_in_z_filename, self.pr_i_in_z)
            write_obj(z_filename, self.pz)
            write_obj(pr_filename, self.pr)
            write_obj(z_in_u_filename, self.pr_z_in_u)
        print(self.pz)

    @staticmethod
    def init_data(topic_num, checks):
        # 统计
        users = set()
        items = set()
        u_i_pairs = set()
        for u, u_checks in checks.items():
            users.add(u)
            for check in u_checks:
                i = check[0]
                u_i_pair = (u, i)
                items.add(i)
                u_i_pairs.add(u_i_pair)

        # 初始化参数 随机数
        pr_u_in_z = {}
        pr_i_in_z = {}
        pz = {}
        pr = {}
        for z in range(topic_num):
            pr_u_in_z[z] = {}
            pr_i_in_z[z] = {}
            pz[z] = random()
            for item in items:
                pr_i_in_z[z][item] = random()
            for user in users:
                pr_u_in_z[z][user] = random()
            dic_value_reg_one(pr_u_in_z[z])
            dic_value_reg_one(pr_i_in_z[z])
        dic_value_reg_one(pz)
        for pair in u_i_pairs:
            pr[pair] = {}
            for z in range(topic_num):
                pr[pair][z] = random()
            dic_value_reg_one(pr[pair])
        return pr_u_in_z, pr_i_in_z, pz, pr

    @staticmethod
    def e_step(pr_u_in_z, pr_i_in_z, pz, pr):
        print('E')

        for pair in pr.keys():
            u, i = pair
            for z in pz.keys():
                pr[pair][z] = pz[z] * pr_u_in_z[z][u] * pr_i_in_z[z][i]
            dic_value_reg_one(pr[pair])

    @staticmethod
    def m_step(pr_u_in_z, pr_i_in_z, pz, pr, checks):
        print('M')
        for z in pz.keys():
            pz[z] = 0
            for pair in pr.keys():
                pz[z] += pr[pair][z]
        dic_value_reg_one(pz)

        for z in pr_u_in_z.keys():
            for u in pr_u_in_z[z].keys():
                pr_u_in_z[z][u] = 0
                for check in checks.get(u):
                    i = check[0]
                    pr_u_in_z[z][u] += pr[(u, i)][z]

            dic_value_reg_one(pr_u_in_z[z])

        for z in pr_u_in_z.keys():
            for i in pr_i_in_z[z].keys():
                pr_i_in_z[z][i] = 0
            for u in pr_u_in_z[z].keys():
                for check in checks.get(u):
                    i = check[0]
                    pr_i_in_z[z][i] += pr[(u, i)][z]
            dic_value_reg_one(pr_i_in_z[z])

    @staticmethod
    def l(pr_u_in_z, pr_i_in_z, pz, checks):
        sumv = .0
        for u in checks.keys():
            for check in checks[u]:
                i = check[0]
                temp = .0
                for z in pz.keys():
                    temp += pz[z] * pr_u_in_z[z][u] * pr_i_in_z[z][i]
                sumv += log(temp)
        return sumv

    @staticmethod
    def em_loop(pr_u_in_z, pr_i_in_z, pz, pr, checks, max_loop=200, stop_delta=2):
        count = 0
        pre_l = 0
        while count < max_loop:
            MyLDA.e_step(pr_u_in_z, pr_i_in_z, pz, pr)
            MyLDA.m_step(pr_u_in_z, pr_i_in_z, pz, pr, checks)
            l = MyLDA.l(pr_u_in_z, pr_i_in_z, pz, checks)
            if abs(l - pre_l) < stop_delta:
                return
            pre_l = l
            print(l)
            print(pz)
            count += 1

    def predict(self, u, i):
        p = 0
        for z in self.pz.keys():
            p += self.pz[z] * self.pr_u_in_z[z][u] * self.pr_i_in_z[z][i]
        return p

    def sim(self, u1, u2):
        return cosine_for_dic(self.pr_z_in_u[u1], self.pr_z_in_u[u2])


def recommend(checks, sim_mat, topn, predict_fun):
    rec = {}
    for u in sim_mat:
        count = 0
        rec[u] = {}
        for uss in sim_mat[u]:
            count += 1
            if count >= topn:
                break
            for (item, score, time) in checks[uss[0]]:
                if not rec[u].keys().__contains__(item):
                    rec[u][item] = predict_fun(u, item)

    for user in rec.keys():
        rec[user] = sort_dict(rec[user])
    # print(rec[0])
    return rec


# main
def cf_main(train_file, test_file, topns=None, topks=None):
    if topks is None:
        topks = [20]
    if topns is None:
        topns = [20]
    nprs = []
    nres = []
    print('read_table')
    table = read_checks_table(train_file, uin=0, iin=4, timein=1, scorein=None)
    test = read_checks_table(test_file, uin=0, iin=4, timein=1, scorein=None)
    friends_dic = read_dic_set('Gowalla_edges.txt')
    if not os.path.exists('mid_data/' + '-'.join(train_file.split('.')[:-1]) + '/'):
        os.mkdir('mid_data/' + '-'.join(train_file.split('.')[:-1]) + '/')
    # ========= LDA ================
    lda = MyLDA(train_filename=train_file, topic_num=8)
    sim_fun = lambda u1, u2: lda.sim(u1, u2)
    sim_fun_name = 'lda' + str(lda.topic_num) + 't'
    predict_fun = lda.predict

    dir_name = 'mid_data/' + '-'.join(train_file.split('.')[:-1]) + '/' + sim_fun_name +'/'
    sim_name = dir_name + 'sim.txt'

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    if os.path.exists(sim_name):
        print('read sim metrics from file')
        sim_metrics = read_obj(sim_name)
    else:
        print('cal_sim_mat')
        sim_metrics = cal_sim_mat(table, similar_fun=sim_fun)
        write_obj(sim_name, sim_metrics)
    for topn in topns:
        rec_name = dir_name + '-'.join(['rec', sim_fun_name, str(topn)]) + '.txt'
        ex_rec_name = dir_name + '-'.join(['ex_rec', sim_fun_name, str(topn)]) + '.txt'
        if os.path.exists(ex_rec_name):
            print('read recommend result from file')
            rec = read_obj(ex_rec_name)
        else:
            print('recommend')
            rec = recommend(table, sim_metrics, topn, predict_fun)
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
    return nprs, nres


if __name__ == '__main__':
    nprs, nres = cf_main('all-trainklnd-Gowalla_totalCheckins.txt',
                         'all-testklnd-Gowalla_totalCheckins.txt',
                         topns=[5, 10, 15, 20, 25, 30],
                         topks=[5, 10, 15, 20, 25])
    pprint(nprs)
    pprint(nres)