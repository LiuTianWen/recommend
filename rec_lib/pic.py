# -*- coding:utf-8 -*-

def line(data, line_names, xlias, ymax=0.3, ymin=0):
    import matplotlib.pyplot as plt
    markers = ['o', '*', 'D', 'd', 's', 'p', '^', 'H', 'h']
    plt.title('recall')
    plt.ylim(ymax=ymax, ymin=ymin)
    plt.xlim(xmax=max(xlias)+1)
    for i in range(len(data)):
        plt.plot(xlias, data[i], marker=markers[i], label=line_names[i])
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
    plt.legend()    
    plt.tight_layout()    
    plt.show()  

if __name__ == '__main__':
    # data = [
    #     [0.271, 0.1794, 0.1408, 0.1002, 0.0797, 0.0653, 0.0519, 0.0433],
    #     [0.2581, 0.1802, 0.1433, 0.1055, 0.0863, 0.0684, 0.0546, 0.0454],
    #     [0.1438, 0.1071, 0.0936, 0.0755, 0.0665, 0.0556, 0.0449, 0.0385],
    #     [0.1113, 0.0931, 0.0802, 0.0666, 0.0573, 0.0482, 0.0397, 0.0341],
    #     [0.1741, 0.1294, 0.1067, 0.0861, 0.0739, 0.0618, 0.0497, 0.0419],
    #     [0.1665, 0.1238, 0.1093, 0.0872, 0.0731, 0.0609, 0.0492, 0.0414],
    # ]
    # labels = ['cosine(01)300', 'cosine(fq)300', 'cosine(01)10', 'cosine(fq)10', 'cosine(01)20', 'cosine(fq)20' ]
    # xlias = [1, 2, 3, 5, 7, 10, 15, 20]
    # bar(data, labels, xlias, 0.5, 0, 'topk', 'precision', 'compare fq 01')
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
    # line(recall, line_names, xlias, ymax=0.1)
    te()