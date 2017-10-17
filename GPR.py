from rec_lib.evaluate import precision, recall
from rec_lib.geo_inf import GeoInf
from rec_lib.utils import read_checks_table, sort_dict, read_obj


def read_center(filename, split_sig=',', oin=0, lain=1, loin=2):
    centers = {}
    with open(filename) as f:
        for each in f:
            elements = each.strip().split(split_sig)
            o = elements[oin]
            la = float(elements[lain])
            lo = float(elements[loin])
            centers[o] = [la, lo]
    return centers

def read_location_users(filename, split_sig=',', uin=0, iin=4):
    loc_users = {}
    with open(filename) as f:
        for each in f:
            elements = each.strip().split(split_sig)
            u = elements[uin]
            i = elements[iin]
            # lo = float(elements[loin])
            if loc_users.get(i) is not None:
                loc_users[i].add(u)
            else:
                loc_users[i] = set([u])
    return loc_users

train_file = 'trainRF-NA-Gowalla_totalCheckins.txt'
test_file = 'testRF-NA-Gowalla_totalCheckins.txt'

# train_file = 'trainRF-SH-FoursquareCheckins.csv'
# test_file = 'testRF-SH-FoursquareCheckins.csv'

# table = read_checks_table(train_file, split_sig=',', uin=0, iin=4, timein=3, scorein=None, time_format='%Y-%m-%d %H:%M:%S', lain=1, loin=2)
# test = read_checks_table(test_file, split_sig=',', uin=0, iin=4, timein=3, scorein=None, time_format='%Y-%m-%d %H:%M:%S', lain=1, loin=2)

table = read_checks_table(train_file, split_sig='\t', uin=0, iin=4, timein=1, scorein=None, time_format='%Y-%m-%dT%H:%M:%SZ', lain=2, loin=3)
test = read_checks_table(test_file, split_sig='\t', uin=0, iin=4, timein=1, scorein=None, time_format='%Y-%m-%dT%H:%M:%SZ', lain=2, loin=3)

# loc_center = read_center('trainRF-SH-FoursquareLocationCenter.csv')
# user_center = read_center('trainRF-SH-FoursquareUserCenter.csv')

loc_center = read_center('trainRF-NA-Gowalla_LocCenter.txt')
user_center = read_center('trainRF-NA-Gowalla_UserCenter.txt')

# 这个流行度好像和 距离没法融合
# loc_users = read_location_users(train_file)
# maxu = max([len(users) for loc, users in loc_users.items()])
# pop_inf = {loc: len(users)/maxu for loc, users in loc_users.items()}

# rec_file = 'mid_data/trainRF-SH-FoursquareCheckins/0.5-0.3-soc0.5-sq_score1d-cosine_1/[0.3, 0.2, 0.5]/ex_rec-5.txt'
rec_file = 'mid_data/trainRF-NA-Gowalla_totalCheckins/0.5-0.3-soc0.5-sq_score1d-cosine_1/[0.3, 0.1, 0.6]/ex_rec-5.txt'

orec = read_obj(rec_file)

geo_inf = GeoInf(a=0.84534522188, b=-1.61667304945, checks=table, loc_center=loc_center, user_center=user_center)
# geo_inf = GeoInf(a=0.651, b=-1.628, checks=table, loc_center=loc_center, user_center=user_center)

# locs = set(loc_center.keys())

# users = ["11823", "10362", "11588", "16457", "2738", "7380", "1676", "2270", "9429", "10650", "9488", "10320", "2461", "4330", "9565", "8895", "16248", "16201", "16633", "14710", "9632", "4962", "10579", "16057", "7836", "4971", "12417", "6791", "16181", "6533", "322", "132", "11998", "2882", "10184", "15244", "15469", "9210", "15982", "685", "1147", "7313", "6390", "11391", "13552", "4421", "11881", "2953", "10025", "4610", "15455", "7744", "11512", "13107", "11328", "2153", "2150", "13310", "10554", "17003", "4343", "17836", "13097", "3510", "7806", "15655", "70", "15838", "17717", "17390", "4282", "16446", "15078", "6074", "9504", "12785", "740", "8525", "16427", "2188", "11119"]

# rate = 0
pre = []
re = []
for rate in [3]:
    rate /= 10
    rec = {}
    for u in orec.keys():
        rec[u] = {p[0]:p[1] for p in orec[u]}
        inf = geo_inf(u, rec[u].keys())
        for l in inf.keys():
            rec[u][l] = rate*rec[u].get(l, 0) + (1-rate)*inf[l]
        rec[u] = sort_dict(rec[u])

    pre.append(precision(rec, test_table=test, topk=10))
    re.append(recall(rec, test_table=test, topk=10))
print(pre)
print(re)