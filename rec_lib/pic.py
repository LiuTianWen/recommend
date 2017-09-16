# -*- coding:utf-8 -*-


def bar():
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    # 必须配置中文字体，否则会显示成方块
    # 注意所有希望图表显示的中文必须为unicode格式

    font_size = 10  # 字体大小
    fig_size = (8, 6)  # 图表大小

    names = ('k=4', 'k=8', 'k=12', 'k=16', 'k=24', 'k=32')  # 姓名
    subjects = ('5', '10', '20')  # 科目
    y1 = [0.053, 0.041, 0.027, ]
    y2 = [0.066, 0.045, 0.031, ]
    y3 = [0.067, 0.044, 0.030, ]
    y4 = [0.069, 0.046, 0.034, ]
    y5 = [0.062, 0.042, 0.030, ]
    y6 = [0.059, 0.040, 0.030, ]
    # 图表标题
    plt.title('')
    scores = (y1, y2, y3, y4, y5, y6)  # 成绩

    # 更新字体大小
    mpl.rcParams['font.size'] = font_size
    # 更新图表大小
    mpl.rcParams['figure.figsize'] = fig_size
    # 设置柱形图宽度
    bar_width = 0.15

    index = np.arange(len(scores[0]))
    # 绘制「小明」的成绩
    rects1 = plt.bar(index, scores[0], bar_width, color='#0072BC', label=names[0])
    # 绘制「小红」的成绩
    rects2 = plt.bar(index + bar_width * 1, scores[1], bar_width, color='#E01C24', label=names[1])
    # 绘制「小红」的成绩
    rects3 = plt.bar(index + bar_width * 2, scores[2], bar_width, color='#0D1C24', label=names[2])
    # 绘制「小红」的成绩
    rects4 = plt.bar(index + bar_width * 3, scores[3], bar_width, color='#ED1024', label=names[3])
    # 绘制「小红」的成绩
    rects5 = plt.bar(index + bar_width * 4, scores[4], bar_width, color='#001C04', label=names[4])
    # 绘制「小红」的成绩
    rects5 = plt.bar(index + bar_width * 5, scores[5], bar_width, color='#001004', label=names[5])
    # 绘制「小红」的成绩

    # X轴标题
    plt.xticks(index + bar_width, subjects)
    # Y轴范围
    plt.ylim(ymax=0.1, ymin=0)
    # 图例显示在图表下方
    plt.legend(loc=0)
    plt.xlabel('rec_num')

    # 添加数据标签
    def add_labels(rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')
            # 柱形图边缘用白色填充，纯粹为了美观
            rect.set_edgecolor('white')

    add_labels(rects1)
    add_labels(rects2)
    add_labels(rects3)
    add_labels(rects4)
    add_labels(rects5)

    # 图表输出到本地
    plt.show()


def line():
    import matplotlib.pyplot as plt
    nes = [5, 10, 15]
    x = [5, 10, 15, 20, 25]
    markers = ['o', '*', 'D', 'd', 's', 'p']
    index = ['U-CF', 'S-CF', 'T-CF', 'SVD']
    # index = ['U-CF','S-CF','TT-CF']
    plt.title('recall')
    ys = [[0.0519, 0.0704, 0.0854, 0.0963, 0.1033],
          [0.0585, 0.0836, 0.1023, 0.1141, 0.124],
          [0.0643, 0.0918, 0.1117, 0.1245, 0.1359], ]
    # [0.0453, 0.0658, 0.079, 0.0905, 0.092]]

    # x = np.linspace(0, 2 * np.pi, 100)
    # Y轴范围
    plt.ylim(ymax=0.3, ymin=0)
    for i in range(len(ys)):
        print(i)
        plt.plot(x, ys[i], marker=markers[i], label=index[i])
    # plt.plot(x, y2, label='y = cos(x)')
    plt.legend()
    plt.show()
    # plt.show()


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


if __name__ == '__main__':
    line()
