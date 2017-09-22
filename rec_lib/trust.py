from pprint import pprint

from rec_lib.utils import sort_dict


class TrustCalculator:
    def __init__(self, friend_dic, max_depth=4, decay=2 / 3):
        self.friend_dic = friend_dic
        self.max_depth = max_depth
        self.decay = decay
        self.sim_mat = {}

    @property
    def name(self):
        return 'trust-' + str(self.max_depth) + '-' + str(self.decay)

    def get_relative_friends(self, u):

        old_nodes = set([u])
        floors = [{} for i in range(self.max_depth + 1)]
        floors[0][u] = 1

        for i in range(self.max_depth):
            tmp = set()
            for df in floors[i].keys():
                for f in self.friend_dic[df].keys():
                    if f not in old_nodes:
                        if floors[i + 1].__contains__(f):
                            floors[i + 1][f][0] += floors[i][df] * self.friend_dic[df][f]
                            floors[i + 1][f][1] += floors[i][df]
                        else:
                            floors[i + 1][f] = [floors[i][df] * self.friend_dic[df][f], floors[i][df]]
                        tmp.add(f)
                        # print('f', f, floors[i + 1][f])
            for k, v in floors[i + 1].items():
                floors[i + 1][k] = v[0] / v[1]
            old_nodes.update(tmp)
        # print(floors)
        sim_list = {}
        d = 1 / self.decay
        for i in range(1, self.max_depth + 1):
            d *= self.decay
            for f, v in floors[i].items():
                # print('v', v)
                sim_list[f] = v * d
                # print(sim_list)
        # sim_list = sort_dict(sim_list)

        return sim_list

    def cal_sim_mat(self, users):
        users = set(users)
        import multiprocessing
        def worker(users, lock):
            while users:
                with lock:
                    if users:
                        user = users.pop()
                    else:
                        user = None
                if user is not None:
                    self.sim_mat[user] = self.get_relative_friends(user)

        lock = multiprocessing.Lock()
        for i in range(20):
            a = multiprocessing.Process(worker(users, lock))
            a.start()

    def sim(self, u1, u2):
        if not self.sim_mat.__contains__(u1):
            print(len(self.sim_mat))
            self.sim_mat[u1] = self.get_relative_friends(u1)
        return self.sim_mat.get(u1, {}).get(u2, 0)


if __name__ == '__main__':
    friend_dic = {
        'A': {'B': 1, 'C': 1},
        'B': {'A': 1, 'H': 1, 'D': 1, 'F': 1},
        'C': {'A': 1, 'G': 1, 'E': 1, 'D': 0.2},
        'D': {'B': 1, 'H': 1},
        'E': {'C': 1},
        'F': {'B': 1, 'H': 1},
        'G': {'C': 1},
        'H': {'B': 1, 'D': 1, 'F': 1}
    }
    md = 3
    decay = 1
    tc = TrustCalculator(friend_dic, md, decay)
    pprint(tc.sim_mat)
    print(tc.sim('A', 'C'))
