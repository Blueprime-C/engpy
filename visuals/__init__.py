from matplotlib import pyplot as plt
from matplotlib import style
from misc.miscs import nums, alnums
from misc.vars import greek_map, alpha


class Visualize:
    
    def __init__(self, var, obj='', color='g', sec='', linewidth=2, *args, **kwargs):
        self.color = color if color else alpha
        self.linewidth = linewidth
        self.var = var
        self.kwargs = kwargs
        self.args = args
        self.obj = obj
        self.sec = sec

    @property
    def plot(self):
        style.use('ggplot')
        var_ = list(self.var)[0]
        if var_ in greek_map:
            var_ = greek_map[var_]
        tab = self.obj.tables(self.var)
        xaxis = alnums(*list(tab))
        yaxis = alnums(*tab.values())
        while 'nil' in yaxis:
            i = yaxis.index('nil')
            del xaxis[i]; del yaxis[i]

        while None in yaxis:
            i = yaxis.index(None)
            del xaxis[i]; del yaxis[i]

        plt.plot(xaxis, yaxis, self.color,
                 label = 'Expression', linewidth = self.linewidth, *self.args, **self.kwargs)
        plt.title(f'Graph of {repr(self.obj)}')
        plt.ylabel(f'F({var_})')
        plt.xlabel(var_)
        
        plt.grid(True, color = 'k')

        plt.show()

    @property
    def multiplot(self):
        style.use('ggplot')
        var_ = list(self.var)[0]
        if var_ in greek_map:
            var_ = greek_map[var_]
        e_list = []
        for counts, eqns in enumerate(self.obj):
            if self.sec:
                name_e = repr(eqns)
                eqns = eqns.subject(self.sec)
             

            tab = eqns.tables(self.var)
            xaxis = alnums(*list(tab))
            yaxis = alnums(*tab.values())
            while 'nil' in yaxis:
                i = yaxis.index('nil')
                del xaxis[i]; del yaxis[i]

            while None in yaxis:
                i = yaxis.index(None)
                del xaxis[i]; del yaxis[i]

            plt.plot(xaxis, yaxis, self.color[counts + 2],
                    label = f'{eqns}' if not self.sec else name_e, linewidth = self.linewidth, *self.args, **self.kwargs)
            e_list.append(repr(eqns) if not self.sec else name_e)
        plt.title(f'Graph of {", ".join(e_list)}')
        
        if not self.sec:
            vy = eqns.vars
            vy.remove(str(var_))
            vy = vy[0] if vy else 'y'
        else:
            vy = self.sec
        plt.ylabel(f'{vy}')
        plt.xlabel(var_)
        
        plt.legend()
        plt.grid(True, color = 'k')

        plt.show()
