from pprint import pprint

import matplotlib.pyplot as plt
from numpy import *
import numpy as np

from rec_lib.utils import read_checks_table


def cal_center(check_positions):
    checks = mat(check_positions)
    checks = checks.T
    center = cal_center_average(check_positions)
    center2 = cal_center_split(check_positions)
    print('c', center)
    plt.scatter(checks[0], checks[1])
    plt.scatter([center[0]], [center[1]], marker='*', c='r', s=100)
    plt.scatter([center2[0]], [center2[1]], marker='>', c='r', s=100)
    plt.show()


def press(event):
    global i
    global loc_user_pos
    global loc_center
    if event.inaxes == None:
        if i > 0:
            i -= 1
        else:
            i = 0
    else:
        i += 1
        while len(loc_user_pos.get(locations[i])) < 15:
            i += 1
        print("next")
    fig = event.inaxes.figure
    ax = fig.add_subplot(111)
    # checks = []
    plt.clf()
    checks = mat(loc_user_pos.get(locations[i])).T
    print(checks)
    plt.scatter(checks[0], checks[1])
    plt.scatter([loc_center[locations[i]][0]], [loc_center[locations[i]][1]], marker='*', c='r', s=100)
    fig.canvas.draw()


def cal_center_average(check_points):
    checks = mat(check_points)
    checks = checks.T
    return [average(checks[0]), average(checks[1])]


def cal_center_split(checks_points):
    print('all', checks_points)
    if len(checks_points) == 1:
        return checks_points[0]
    check_t = mat(checks_points).T
    x_center = average(check_t[0])
    y_center = average(check_t[1])
    areas = [[], [], [], []]
    for pos in checks_points:
        if pos[0] > x_center:
            if pos[1] > y_center:
                areas[0].append(pos)
            else:
                areas[1].append(pos)
        else:
            if pos[1] > y_center:
                areas[2].append(pos)
            else:
                areas[3].append(pos)
    areas.sort(key=lambda d: len(d), reverse=True)
    # pprint(areas)
    if len(areas[0]) == len(checks_points):
        return checks_points[0]
    else:
        return cal_center_split(areas[0])


def read_checks_pos(filename, split_sig=',', uin=0, lain=1, loin=2):
    table = {}
    with open(filename) as f:
        for each in f:
            elements = each.strip().split(split_sig)
            u = elements[uin]
            la = float(elements[lain])
            lo = float(elements[loin])
            if table.get(u) is not None:
                table[u].append([la, lo])
            else:
                table[u] = [[la, lo]]
    return table


def read_location_pos(filename, split_sig=',', iin=4, lain=1, loin=2):
    table = {}
    with open(filename) as f:
        for each in f:
            elements = each.strip().split(split_sig)
            i = elements[iin]
            la = float(elements[lain])
            lo = float(elements[loin])
            if table.get(i) is not None:
                table[i].append([la, lo])
            else:
                table[i] = [[la, lo]]
    return table


def read_user_center(filename, split_sig=',', uin=0, lain=1, loin=2):
    table = {}
    with open(filename) as f:
        for each in f:
            elements = each.strip().split(split_sig)
            u = elements[uin]
            la = float(elements[lain])
            lo = float(elements[loin])
            table[u] = [la, lo]
    return table


def read_location_users(filename, split_sig=',', uin=0, iin=4):
    table = {}
    with open(filename) as f:
        for each in f:
            elements = each.strip().split(split_sig)
            u = elements[uin]
            i = elements[iin]
            # lo = float(elements[loin])
            if table.get(i) is not None:
                table[i].add(u)
            else:
                table[i] = set([u])
    return table

def get_location_user_pos(location_users:dict, user_center:dict):
    table = {}
    for loc, users in location_users.items():
        table[loc] = []
        for u in users:
            table[loc].append(user_center.get(u))
    return table

# table = read_checks_pos('trainna-FoursquareCheckins.csv')
# location = read_location_pos('../trainna-FoursquareCheckins.csv')

#
i = 0
# users = list(table.keys())
# ls = list(location.keys())

user_center = read_user_center('trainna-FoursquareUserCenter.csv')
location_users = read_location_users('trainna-FoursquareCheckins.csv')
locations = list(location_users.keys())
loc_user_pos = get_location_user_pos(location_users, user_center)
loc_center = read_user_center('trainna-FoursquareLocationCenter.csv')
#
# # pprint(loc_user_pos)
# print(location_users.get('88153'))
# print(user_center.get('8488'))
# print(table.get('8488'))
if __name__ == '__main__':
    #
    fig = plt.figure()
    fig.canvas.mpl_connect('button_press_event', press)
    ax1 = fig.add_subplot(111)
    plt.show()
    # points = [[a, b] for a in range(5) for b in range(5)]
    # cal_center(check_positions=points)
    # global table
    #
    # with open('trainna-FoursquareUserCenter.csv', 'w') as f:
    #     for user, checks in table.items():
    #         center = cal_center_average(checks)
    #         f.write(",".join([user, str(center[0]), str(center[1])]))
    #         f.write('\n')
    # with open('trainna-FoursquareLocationCenter.csv', 'w') as f:
    #     for item, checks in location.items():
    #         center = cal_center_average(checks)
    #         f.write(",".join([item, str(center[0]), str(center[1])]))
    #         f.write('\n')
