from misc.gen import start_alpha_index
from misc.miscs import num, alnum
from misc.abilities import numable
from misc.gen import getter


class iter2:
    def __init__(self, expr):
        self.expr = expr
        self.it = self.get()

    def get(self):
        for coeff in self.expr.expr:
            if not coeff:
                continue
            for expr in self.expr.expr[coeff]:
                yield self.expr.recreate({coeff: [expr]})

    def __next__(self):
        return next(self.it)

    def __iter__(self):
        return self


class iter1:
    def __init__(self, expr):
        self.expr = expr
        self.it = self.get()
        
    def get(self):
        for coeff in self.expr.expr:
            disp = ''; disp_ = ''
            if not coeff:
                continue
            if coeff < 0:
                disp_ = f' - {abs(num(coeff))}' if coeff != -1 else ' - 1 ' if self.expr.expr[coeff][0] == {'': 0} else ' - '
            else:
                disp_ = f'{coeff}' if coeff != 1 else ' 1 ' if coeff == 1 and self.expr.expr[coeff][0] == {'': 0} else ''
            for count,expr_ in enumerate(self.expr.expr[coeff]):
                _var__ = ''; emb = 0
                if count:
                    disp_ = f' - ' if coeff == -1 and self.expr.expr[coeff][count] != {'':0} else f' - {abs(num(coeff))}' if coeff < 0 else f'{coeff}' if coeff > 0 and coeff != 1 else ' 1 ' if self.expr.expr[coeff][count] == {'':0} else '' 
                for count_, var in enumerate(expr_):
                    _var__ = ''
                    if var and not expr_[var]:
                        continue
                    _var__ = f'({var})' if len(var) > 1 or '/' in format(var) else f'{var}' if not coeff - 1  and not isinstance(var,str) else f'({var})' if not isinstance(var,str) and expr_[var] != 1 else f'{var}'
                    if not isinstance(var,str) and len(var) == 1:
                        if getter(var,'name') == 'Expr':
                            if var._coeff - 1 and not numable(var):
                                coeff *= var._coeff; emb = 1
                        else:
                            if var.coeff - 1:
                                coeff *= var.coeff; emb = 1
                                
                                coeff = ' - ' if coeff == -1 else self.expr.recreate(str(coeff))
                                
                                _var__ = _var__[start_alpha_index(_var__):]
                    if expr_[var] != 1 and expr_[var]:
                        pow_ = f"{expr_[var]}"
                        pow_ = '^' + pow_ if len(pow_) == 1 else f'^({pow_})'
                        _var__ += pow_
                    disp_ += _var__

                yield (f'{coeff}' if not str(coeff).replace(' ', '')[0].isalnum() else f' + {coeff}') if emb else disp_

    def __next__(self):
        return next(self.it)

    def __iter__(self):
        return self


def rep_coeff(expr):
    coeff = expr._coeff
    return expr.recreate({1: expr.expr[coeff]}), coeff


class Range:
    def __init__(self, start = 0, end = '', step = 1):
        start = alnum(start); end = alnum(end); step = alnum(step)
        if not end and start:
            end = start
            start = 0
        self.end = end   
        self.start = start
        self.step = step
        self.state = self.start - self.step

    def __str__(self):
        step = f', {self.step}' if self.step != 1 else ''
        return f'Range({self.start}, {self.end}{step})'

    def __iter__(self):
        self.state = self.start - self.step

        def _next(self):
            while True:
                self.state += self.step
                if self.state > self.end:
                    self.state = self.start - self.step
                    break
                if getter(self.state, 'name'):
                    self.state = self.state.simp()
                yield self.state
        self.iter = _next(self)
        return self

    def __next__(self):
        return next(self.iter)

    __repr__ = __str__


class mat_iter:
    def __init__(self, Mat):
        self.n = 1
        self.stop = Mat.rows
        self.step = 1
        self.Mat = Mat
        
    def __next__(self):
        if self.n > self.stop:
            raise StopIteration
        row = self.Mat.get_row(self.n)
        self.n += self.step
        return row
    
    def __iter__(self):
        return self


class element:
    def __init__(self, Mat):
        self.n = 1
        self.stop = len(Mat)
        self.step = 1
        self.Mat = Mat
        
    def __next__(self):
        if self.n > self.stop:
            raise StopIteration
        row = self.Mat[self.n]
        self.n += self.step
        return row
    
    def __iter__(self):
        return self


class mat_iter_col:
    def __init__(self, Mat):
        self.n = 1
        self.stop = Mat.cols
        self.step = 1
        self.Mat = Mat
        
    def __next__(self):
        if self.n > self.stop:
            raise StopIteration
        row = self.Mat.get_col(self.n)
        self.n += self.step
        return row
    
    def __iter__(self):
        return self

