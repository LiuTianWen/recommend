# -*- coding:utf-8 -*-

def line(data, line_names, xlias, ymax=0.3, ymin=0):
    import matplotlib.pyplot as plt
    markers = ['o', '*', 'D', 'd', 's', 'p', '^', 'H', 'h']
    plt.title('recall')
    plt.ylim(ymax=ymax, ymin=ymin)
    for i in range(len(data)):
        plt.plot(xlias, data[i], marker=markers[i], label=line_names[i])
    plt.legend()
    plt.show()


def te():
    import numpy as np
    import matplotlib.pyplot as plt
    frame = plt.gca()
    x = np.linspace(-0, 10, 100)
    a = 5
    b = 1
    y1 = 1 - (1 / (1 + np.exp(-(b * x - a * b))))
    frame.axes.get_xaxis().set_visible(False)
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
    opacity = 0.4
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
    data = [
        [0.271, 0.1794, 0.1408, 0.1002, 0.0797, 0.0653, 0.0519, 0.0433],
        [0.3323, 0.1734, 0.1214, 0.0775, 0.0583, 0.0434, 0.0327, 0.0277]
    ]
    labels = ['cosine300', 'mf-sim300']
    xlias = [1, 2, 3, 5, 7, 10, 15, 20]
    bar(data, labels, xlias, 0.5, 0, 'topk', 'precision', 'compare mf cosine')
