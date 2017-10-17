from pprint import pprint

from rec_lib.utils import sort_dict



class KatzCalculator:
    def __init__(self, friend_dic:dict, max_depth=3, decay=2/3):
        self.friend_dic = friend_dic
        self.max_depth = max_depth
        self.decay = decay
        self.sim_mat = {}
        self.cal_sim_mat(friend_dic.keys())

    @property
    def name(self):
        return 'trust-' + str(self.max_depth) + '-' + str(self.decay)

    def get_relative_friends(self, u):
        old_nodes = {u}
        floors = [{} for i in range(self.max_depth + 1)]
        floors[0][u] = 1

        for i in range(self.max_depth):
            tmp = set()
            for df in floors[i].keys():
                for f in self.friend_dic.get(df, set()):
                    if f not in old_nodes:
                        if floors[i + 1].__contains__(f):
                            floors[i + 1][f] += 1
                        else:
                            floors[i + 1][f] = 1
                        tmp.add(f)
            old_nodes.update(tmp)
        sim_list = {}
        d = 1 / self.decay
        for i in range(1, self.max_depth + 1):
            d *= self.decay
            for f, v in floors[i].items():
                sim_list[f] = v * d

        return sim_list

    def cal_sim_mat(self, users):
        print('cal')
        t = len(users)
        c = 0
        for user in users:
            c += 1
            self.sim_mat[user] = self.get_relative_friends(user)
            if c % 100 == 0:
                print(c, t)
    def sim(self, u1, u2):
        if not self.sim_mat.__contains__(u1):
            print(len(self.sim_mat))
            self.sim_mat[u1] = self.get_relative_friends(u1)
        return self.sim_mat.get(u1, {}).get(u2, 0)


if __name__ == '__main__':
    friend_dic = {
        'A': {'B','C'},
        'B': {'A', 'H', 'D', 'F'},
        'C': {'A', 'G', 'E', 'D'},
        'D': {'B', 'H'},
        'E': {'C'},
        'F': {'B', 'H'},
        'G': {'C'},
        'H': {'B', 'D', 'F'}
    }
    md = 2
    decay = 0.5
    tc = KatzCalculator(friend_dic, md, decay)
    pprint(tc.sim_mat)
    print(tc.sim('A', 'C'))
