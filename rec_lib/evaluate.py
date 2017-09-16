import math
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from random import random   
import sys
import functools
from datetime import datetime
import pickle


# 计算准确率
# topk 推荐数量
def precision(rec, test_table, topk):
    test = {}
    for k, v in test_table.items():
        test[k] = {e[0] for e in v}
        
    down = 0
    up = 0
    for k,v in rec.items():
        v = set([e[0] for e in v][:topk])
        down += len(v)
        up += len(v & test.get(k,set()))
    # print(up, down)
    return up/down


# 计算召回
# topk 推荐数量
def recall(rec, test_table, topk):
    test = {}
    down = 0
    for k, v in test_table.items():
        test[k] = {e[0] for e in v}
        down += len(test[k])
    
    up = 0
    for k,v in rec.items():
        v = set([e[0] for e in v][:topk])
        up += len(v & test.get(k,set()))
    # print(up, down)
    return up/down

