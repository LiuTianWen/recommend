# -*- coding:utf-8 -*-
import json

from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def threeDemsion():
    fig = plt.figure()
    ax = Axes3D(fig)
    X = np.arange(-4, 4, 0.25)
    Y = np.arange(-4, 4, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)

    # 具体函数方法可用 help(function) 查看，如：help(ax.plot_surface)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')

    plt.show()



def line(data, line_names, xlias, ymax=0.3, ymin=0):
    import matplotlib.pyplot as plt
    markers = ['o', '*', 'D', 'd', 's', 'p', '^', 'H', 'h']
    plt.title('recall')
    # plt.title('precision')
    plt.ylim(ymax=ymax, ymin=ymin)
    # plt.xlim(xmax=max(xlias)+1)
    for i in range(len(data)):
        plt.plot([1,2,3,4,5,], data[i], marker=markers[i], label=line_names[i])
    plt.xticks([1,2,3,4,5,],xlias)
    plt.legend()
    plt.show()


def te():
    import numpy as np
    import matplotlib.pyplot as plt
    frame = plt.gca()
    x = np.linspace(-0, 48, 100)
    a = 1
    b = 1
    y1 = a * pow(x, -b)
    # frame.axes.get_xaxis().set_visible(False)
    plt.plot(x, y1, c='r', ls='--', lw=3)
    # plt.plot(x, y2, c='#526922', ls='-.')
    plt.show()


def bar(data, labels, xlias, ymax, ymin, xlabel, ylabel, titile):
    import matplotlib as mpl
    import numpy as np
    import matplotlib.pyplot as plt
    n_groups = len(data[0])
    colors = ['r', 'g', 'c', 'm', 'w', 'b', 'y']
    fig, ax = plt.subplots()    
    index = np.arange(n_groups)    
    bar_width = 0.3
    opacity = 0.5
    for n in range(len(data)):
        plt.bar(index+bar_width/2*n, data[n], bar_width/2, alpha=opacity, color=colors[n], label=labels[n])

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titile)
      
    plt.xticks(index - opacity/2 + 2*bar_width, xlias, fontsize =18)
  
    plt.yticks(fontsize =18)
  
    plt.ylim(ymin, ymax)
    plt.legend(loc='upper ')    
    plt.tight_layout()    
    plt.show()  

if __name__ == '__main__':
    # threeDemsion()
    #
    # data = [
    #  [0.1014, 0.0938, 0.0845, 0.0772, 0.0718, 0.0673],
    #  [0.1106, 0.0983, 0.0877, 0.0799, 0.0733, 0.0684],
    #  [0.1109, 0.1014, 0.0912, 0.083, 0.076, 0.0707],
    #  [0.0791, 0.0728, 0.0661, 0.0601, 0.0557, 0.0522],
    #  [0.113, 0.102, 0.0914, 0.084, 0.0773, 0.0719],
    #  [0.0759, 0.0697, 0.0634, 0.0584, 0.0543, 0.0509]]

    '''  Foursqaure eta
    precison = [
        [0.0706, 0.0654, 0.0613, 0.0576, 0.0547, 0.052],
        [0.07, 0.0654, 0.0619, 0.0586, 0.0553, 0.0527],
        [0.0719, 0.0665, 0.0626, 0.059, 0.0558, 0.0531],
        [0.0704, 0.0657, 0.0615, 0.0581, 0.0543, 0.0515],
        [0.0703, 0.0653, 0.0617, 0.0581, 0.0544, 0.0517]
    ]
    recall = [
        [0.0404, 0.0449, 0.0491, 0.0527, 0.0563, 0.0595],
        [0.04, 0.0449, 0.0496, 0.0536, 0.0569, 0.0602],
        [0.0411, 0.0456, 0.0502, 0.0539, 0.0574, 0.0607],
        [0.0402, 0.0451, 0.0492, 0.0531, 0.0559, 0.0589],
        [0.0402, 0.0448, 0.0494, 0.0532, 0.056, 0.0591]
    ]
    '''
    # precison = [
    #     # [0.0303, 0.0286, 0.0277, 0.0272, 0.0262, 0.0251],
    #     # [0.0313, 0.0296, 0.0287, 0.0277, 0.026, 0.0252],
    #     [0.0324, 0.0306, 0.029, 0.0278, 0.0266, 0.0254],
    #     [0.0323, 0.0304, 0.0294, 0.028, 0.0269, 0.0261],
    #     [0.03, 0.029, 0.0284, 0.0272, 0.0259, 0.0248],
    #     [0.0307, 0.0288, 0.0284, 0.0274, 0.0265, 0.0256],
    #     [0.0309, 0.0298, 0.0285, 0.0272, 0.0257, 0.0244],
    # ]
    # recall = [
    #     [0.0044, 0.005, 0.0055, 0.0061, 0.0065, 0.0069],
    #     [0.0044, 0.005, 0.0056, 0.0061, 0.0066, 0.0071],
    #     [0.0041, 0.0047, 0.0054, 0.0059, 0.0063, 0.0068],
    #     [0.0042, 0.0047, 0.0054, 0.006, 0.0065, 0.007],
    #     [0.0042, 0.0049, 0.0054, 0.0059, 0.0063, 0.0067],
    # ]

    precision = [
        [0.0468, 0.0393],
        [0.0411, 0.0349],
        [0.052, 0.04410272669625872],
        [0.0527, 0.0412],
        [0.0670, 0.05364616360177552]
    ]

    # recall = np.mat(recall).T.getA()
    # print(json.dumps(recall))
    # labels = ['$\eta$=0.3', '$\eta$=0.4', '$\eta$=0.5', '$\eta$=0.6', '$\eta$=0.7', '$\eta$=0.8' ]
    # labels = ['UB-CF', 'S-CF', 'G-R', 'STI-CF', 'GSTI-CF', '$\eta$=0.8' ]
    # xlias = ['@5', '@10']
    # # xlias = [5, 6, 7, 8, 9, 10]
    # bar(precision, labels, xlias, 0.08, 0.02, 'topk', 'precision', 'Comparision In Gowalla')
    # bar(recall, labels, xlias, 0.011, 0.002, 'topk', 'recall', 'variable $\eta$ in Gowalla')
    # precision = [[0.1465, 0.0947, 0.0757, 0.0562, 0.0459, 0.0377, 0.0301, 0.0266],
    #  [0.1888, 0.1184, 0.0887, 0.0618, 0.0494, 0.0391, 0.03, 0.0251],
    #  [0.2055, 0.1278, 0.0943, 0.0654, 0.0521, 0.0412, 0.0308, 0.0256],
    #  [0.2064, 0.1264, 0.0936, 0.0647, 0.0525, 0.0414, 0.0313, 0.0256]]
    # recall = [[0.0243, 0.0304, 0.0352, 0.0406, 0.0433, 0.0458, 0.0473, 0.0494],
    #  [0.033, 0.0409, 0.0452, 0.0509, 0.0554, 0.0603, 0.0656, 0.0692],
    #  [0.0362, 0.0449, 0.0491, 0.0557, 0.0608, 0.067, 0.0723, 0.0775],
    #  [0.0377, 0.046, 0.0507, 0.0574, 0.0639, 0.0703, 0.077, 0.0815]]

    # xlias = [1, 2, 3, 5, 7, 10, 15, 20]
    # line_names = ['neibor' + str(e) for e in [5, 10, 15, 20]]
    # line(data, labels, xlias, ymax=0.3)
    # te()
    # precison = [0.07145925819848203, 0.08558881092176238, 0.0901713685617452, 0.0924149124063201, 0.09293999713590148,
    #     0.09260585230798606, 0.09193756265215523, 0.090935128168409, 0.08993269368466275, 0.08926440402883193,
    #     0.08506372619218101,]

    # precison= [0.007117160745788509, 0.008561347677193954, 0.009106160711197206, 0.009140752014943443, 0.008889965062783216, 0.008535404199384275, 0.008319208550970287, 0.008137604206302535, 0.00806842159881006, 0.007938704209761666, 0.007056625964232592]

    # precison= [0.04086814086814087, 0.04892164892164892, 0.05156975156975157, 0.05285285285285285, 0.05315315315315315, 0.05296205296205296, 0.05257985257985258, 0.052006552006552006, 0.051433251433251434, 0.05105105105105105, 0.047747747747747746]

#     precison = [0.05199746353836398,0.06284083703233989,0.06670894102726696,0.06696258719086874,0.06518706404565631,0.06258719086873811,0.061001902346227016,0.05967025998731769,0.05916296766011414,0.058211794546607486,0.051236525047558656,
# ]

    # precison = np.mat(precison).T.getA()
    # xlias = np.arange(0, 1.1, 0.1)
    # labels = xlias
    # plt.bar(left=xlias, height= precison, width=0.05, align='center', color='black')
    # plt.xticks(xlias, labels)
    # plt.ylim((0.03,0.06))
    # plt.xlim((-0.1,1.1))
    # plt.xlabel('$\lambda$')
    # plt.ylabel('recall')
    # # plt.title('precision with $\lambda$ in Gowalla' )
    # plt.title('recall with $\lambda$ in Foursquare' )
    # plt.show()
    # bar(precison, labels, xlias, 0.1, 0.05, 'topk', 'precision', 'topic influence')#


    recall = [
        [0.0043, 0.0034, 0.0028, 0.0024, 0.0020],
        [0.0039, 0.0027, 0.0021, 0.0012, 0.0009]]
    # recall = [
    #     [0.032, 0.027, 0.023, 0.020, 0.017],
    #     [0.027, 0.021, 0.017, 0.010, 0.007]]
    line_names = ['soc-intimacy', 'soc-jaccard']
    line(recall, line_names=line_names, xlias=['100%','50%','30%','20%','10%',], ymax=0.005,ymin=0)