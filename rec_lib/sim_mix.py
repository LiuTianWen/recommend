import numpy as np

from rec_lib.utils import read_obj


def keys_to_index(keys):
    keys = list(keys)
    index = {}
    for i in range(len(keys)):
        index[keys[i]] = i
    return index

def dic_to_mat(index, dic):
    rmat = np.zeros(shape=(len(index), len(index)))
    for u1, uss in dic.items():
        for u2, s in uss.items():
            rmat[index[u1], index[u2]] = s
    return rmat



if __name__ == '__main__':
    sim_map1 = read_obj('../mid_data/trainRF-SH-FoursquareCheckins/1-0.5-0.3-soc-group0-soc-group1-soc-group2/soc-group0')

    sim_map2 = read_obj('../mid_data/trainRF-SH-FoursquareCheckins/1-0.5-0.3-soc-group0-soc-group1-soc-group2/soc-group1')
    # sim_map2 = {u: {f[0]: f[1] for f in fs} for u, fs in sim_map2.items()}
    index= keys_to_index(sim_map1.keys())

    m1 = dic_to_mat(index, sim_map1)
    m2 = dic_to_mat(index, sim_map2)
    m = m1 * 0.5 + m2 *0.5
    print(m)
