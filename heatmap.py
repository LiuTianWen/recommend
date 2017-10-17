import os
import json
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits import axes_grid1
from mpl_toolkits.mplot3d import Axes3D



fr2 = lambda x: float('%.2f' % x)

def get_pr(alpha, beta):
    dir = str([fr2(alpha), fr2(beta), fr2(1- alpha-beta)])
    precision_file = '/'.join([root, dir, 'nprs.txt'])
    print(precision_file)
    if not os.path.exists(precision_file):
        return 0.01
    with open(precision_file) as f:
        precision = json.loads(f.readline())
        return precision[0][0]
    return 0.01

root = 'mid_data/trainRF-NA-Gowalla_totalCheckins/1-0.5-0.3-soc-group0-soc-group1-soc-group2'
mz = 0
mx = 0
my = 0

for i in range(11):
    for j in range(11):
        Z[i, j] = get_pr(X[i, j], Y[i, j])
        if mz < Z[i, j]:
            my = Y[i, j]
            mx = X[i, j]
            mz = Z[i, j]
# ratess = []
# for x in np.arange(0, 1.1, 0.1):
#     for y in np.arange(0, 1.1-x, 0.1):
#         ratess.append([float('%.2f' % x), float('%.2f' % y), float('%.2f' % (1-x-y))])
# X = [r[0] for r in ratess]
# y = [r[1] for r in ratess]
# Z = [r[2] for r in ratess]

print(mx, my, mz)
print(str(Z))
# threeDemsion(X,Y,Z)
data = Z
fig = plt.figure()
grid = axes_grid1.AxesGrid(
    fig, 111, nrows_ncols=(1, 2), axes_pad = 0.5, cbar_location = "right",
    cbar_mode="each", cbar_size="15%", cbar_pad="5%",)

im0 = grid[0].imshow(data, cmap='gray_r', interpolation='nearest')
grid.cbar_axes[0].colorbar(im0)

im1 = grid[1].imshow(data, cmap='jet', interpolation='nearest')
grid.cbar_axes[1].colorbar(im1)
# plt.savefig('/tmp/test.png', bbox_inches='tight', pad_inches=0.0, dpi=200,)
plt.show()