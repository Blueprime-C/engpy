from misc.scan.scan_expr import scan_MD
from errors.exceptions import *
import tools.exprs as expa
from misc.assist import pr_rt
from copy import copy


class surd:
    def __init__(self,exprs):
         if not 'sqrt' in exprs:
             raise UnacceptableToken('No Surd entity is present')
         if '+' in exprs:
            part = exprs.split('+')
            tie = 0
            if not part[0] or part[0] == ' ':
                expr = surd(part[1])
                tie = 1
            else:
                expr = surd(part[0])
            for num, alg in enumerate(part):
                if num-1 < tie:
                    continue
                expr += alg
            self.expr = expr.expr
            return
         exprs = exprs.replace(' ','')
         if exprs[-1] != ')':
            raise UnacceptableToken
         exprs = exprs[:-1]
         exprs = exprs.split('sqrt(')
         expr = {expa.Expr(exprs[0]) if expa.Expr(exprs[0]) else expa.Expr('1'):[{expa.Expr(exprs[1]):expa.Expr('0.5')}]}
         self.expr = expr

    def __str__(self):
        disp = '';
        for coeff in self.expr:
            disp_ = ''
            if not coeff:
                continue
            if (coeff != -1 and coeff != 1) and str(coeff).replace(' ','')[0].isalnum():
                disp_ += ' + '
                if disp: disp += ' + '
            if (coeff == -1 or coeff == 1):
                disp += f'{coeff}'.replace('1','')
            else: disp += str(coeff)
            disp_ += disp
            for count,expr_ in enumerate(self.expr[coeff]):
                if count:
                    disp += disp_
                for var in expr_:
                    if expr_[var] == 0.5:
                        disp += f'sqrt({var})'
                    else:
                        disp += f'{var}' if var else disp_ if not disp else ''
                        if expr_[var] != 1 and expr_[var] != 0:
                            disp += f"^{expr_[var]}"
        if not disp:
            return '0'
        return disp[1:] if disp[0] == ' ' else disp
    
    def __iter__(self):
        return self.loop(self)

    def __mul__(self,other):
        pass
    
    def __sub__(self,other):
        self_ = copy(self)
        if not isinstance(other,surd):
            other = surd(other)
        for coeff,var in other.expr.items():
            if coeff in self.expr:
                for var_ in var:
                    self_.expr[coeff].append(var_)
            else:
                self_.expr[coeff] = var
        return self_
    def __add__(self,other):
        self_ = copy(self)
        if not isinstance(other,surd):
            other = surd(other)
        for coeff,var in other.expr.items():
            if coeff in self.expr:
                for var_ in var:
                    self_.expr[coeff].append(var_)
            else:
                self_.expr[coeff] = var
        return self_

    class loop:
        def __init__(self, cls):
            self.expr = cls.expr
            self.loop = self._loop()
        def _loop(self):
            disp = '';
            for coeff in self.expr:
                if not coeff:
                    continue
                if (coeff == -1 or coeff == 1):
                    disp = f'{coeff}'.replace('1','')
                else:
                    disp = str(coeff)
                for count,expr_ in enumerate(self.expr[coeff]):
                    disp_ = disp
                    for var in expr_:
                        if expr_[var] == 0.5:
                            disp_ += f'sqrt({var})'
                        else:
                            disp_ += f'{var}' if var else str(coeff) if not disp_ else ''
                            if expr_[var] != 1 and expr_[var] != 0:
                                disp_ += f"^{expr_[var]}"
                    yield disp_
        def __next__(self):
            return next(self.loop)
    def __repr__(self):
        return self.__str__()
    def __copy__(self):
        return surd(self.__str__())
    def __format__(self,q):
        form = self.__str__()
        
