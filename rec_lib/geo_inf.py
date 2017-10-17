from rec_lib.geo_distance import haversine


class GeoInf:
    def __init__(self, a, b, checks, loc_center, user_center):
        self.a = a
        self.b = b
        self.checks = checks
        self.loc_center =loc_center
        self.u_base = {}
        self.user_center = user_center
        # print(self.a * pow(1, self.b))

    # def __call__(self, u, locs):
    #     m = 0
    #     inf_table = {}
    #     for loc in locs:
    #         inf = 1
    #         visteds =  set( [check[0] for check in self.checks.get(u)] )
    #         ds = []
    #         for l in visteds:
    #             d = 1+haversine(self.loc_center[loc][0], self.loc_center[loc][1], self.loc_center[l][0], self.loc_center[l][1])
    #             ds.append(d)
    #         ds.sort()
    #         if ds[0] > 100:
    #             continue
    #         for d in ds:
    #             if d == 0:
    #                 print(l, loc, self.loc_center[loc])
    #             else:
    #                 inf *= self.a * pow(d, self.b)
    #         if inf > m:
    #             m = inf
    #         if inf == 1:
    #             raise RuntimeError
    #         inf_table[loc] = inf
    #     for loc in locs:
    #         if inf_table.__contains__(loc):
    #             inf_table[loc] /= m
    #
    #     return inf_table
    #
    def __call__(self, u, locs):
        inf_table = {}
        for loc in locs:
            # inf_table[u] = {}
            d = 1 + haversine(self.loc_center[loc][0], self.loc_center[loc][1], self.user_center[u][0], self.user_center[u][1])
            if d > 0 :
                inf_table[loc] = self.a * pow(d, self.b)
            else:
                inf_table[loc] = self.a
        return inf_table