from matplotlib import plot2d as plt
from matplotlib import style


class Visualize:

    def __init__(self, var, color = 'g', linewidth = 2):
        self.color = color
        self.linewidth = linewidth
        self.var = var

    @property
    def plot(self):

        style.use('ggplot')
        var_ = list(var)[0]
        tab = self.tables(var)
        xaxis = list(tab)
        yaxis = list(tab.values())

        plt.plot(xaxis, yaxis, self.color,
                 label = 'Expression', linewidth = self.linewidth)
        plt.title(format(self))
        plt.ylablel(f'F({var_})')
        plt.xlablel(var_)

        plt.grid(True, color = 'k')

        plt.show()
