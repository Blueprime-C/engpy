import tools.exprs as exprs
from misc.abilities import numable
from misc.miscs import _isinstance
from misc.gen import getter
from misc.scan.scan_expr import scan_MD
from misc.assist import get_den, get_num
from errors.exceptions import *
from copy import copy, deepcopy

class Fraction:
    def __init__(self,num,den = ''):
        self.name = 'Fraction'
        if isinstance(num,list):
            self.num, self.den = num
            return None
        elif isinstance(num,dict):
            self.expr = num
            return
        if not den:
            den = exprs.Expr('1')
        if not getter(num,'name') =='Expr' or not getter(den,'name') =='Expr':
                raise UnacceptableToken(f'Both {num} and {den} must be an Expr object')
        self.expr = {num: den}

    def __str__(self):
        if not self.den:
            return 'inf'
        elif not self.num:
            self.den = exprs.Expr('1')
            return '0'
        num = f'({self.num})' if len(self.num) > 1 else f'{self.num}'
        den = f'({self.den})' if len(self.den) > 1 else f'{self.den}'
        return f'{num}/{den}'

    @property
    def num(self):
        return list(self.expr)[0]

    @property
    def den(self):
        return self.expr[self.num]

    @num.setter
    def num(self, value):
        self.expr = {value: self.den}

    @den.setter
    def den(self, value):
        self.expr = {self.num: value}
    
    def __mul__(self, other):
        
        if not getter(other, 'name') == 'Fraction':
            if '/' in format(other):
                num2 = get_num(other)
                den2 = get_den(other)
            else:
                if numable(other):
                    return Fraction(self.num *other, self.den)

                num2 = exprs.Expr(other)
                if num2 == 1:
                    return copy(self)
                den2 = 1;
        else: den2 = other.den; num2 = other.num
        self_ = self
        pas = False
        den1, num1 = self_.den, self_.num
        if den2 != 1:
            if num1.isdivisible(den2):
                _num = num1 / den2
                if not '/' in format(_num):
                    pas = True
                    num1 = _num; den2 = 1
            if not pas and ((len(num1) == 1 and den2.isfactor(num1)) or (len(num1) > 1 and den2.isdivisible(num1))):
                _num = den2 / num1
                if not '/' in format(_num):
                    num1 = 1; den2 = _num
            pas = False
            
            if num2.isdivisible(den1):
                _num = num2 / den1
                if not '/' in format(_num):
                    pas = True
                    num2 = _num; den1 = 1
            if not pas and ((len(num2) == 1 and den1.isfactor(num2)) or (len(num2) > 1 and den1.isdivisible(num2))):
                _num = den1 / num2
                if not '/' in format(_num):
                    pas = True
                    num2 = 1; den1 = _num
            num = num1 * num2; den = den1 * den2
            return num / den if numable(den) or len(den) == 1 else Fraction(exprs.Expr(num), den)
        if num2.isdivisible(den1):
            _num = num2 / den1
            if '/' not in format(_num):
                return num1 * _num
        elif den1.isdivisible(num2):
            _den = den1 / num2
            _den_ = format(_den)
            if '/' not in _den_ and  not '^-' in _den_:
                den1 = _den; num2 = 1

            num = num1 * num2; den = den1 * den2
            return num / den if len(den) == 1 else Fraction(num, den)
        
        return copy(self)

        

    @property
    def vars(self):
        return self.num.vars + self.den.vars

    @property
    def variables(self):
        return self.num.variables + self.den.variables
    
    
    def __truediv__(self,other):
        if not isinstance(other,Fraction):
            other = Fraction(other)        
        return self * ~other

    def __len__(self):
        return 2
    
    def cal(self,values, desolve = '', desolved = False):
        return self.num.cal(values, desolve = desolve, desolved = desolved)/self.den.cal(values, desolve = desolve, desolved = desolved)
    
    def __add__(self, other):
        
        if not isinstance(other,Fraction):
            other = Fraction(other)
        if self.num == other.num == 0:
            self.den = exprs.Expr('1')
            return self
            
        elif self.num == 0:
            return other
        elif other.num == 0:
            return self
        self_ = copy(self); st = 0
        if '/' not in format(self.den / other.den) and (not '^-' in format(self) and not '^-' in format(self.den / other.den)):
            den = self.den
        elif not '/' in format(other.den / self.den) and (not '^-' in format(other) and not '^-' in format(other.den / self.den)):
            den = other.den
        else:
            st = 1; den = self.den * other.den
        if st:
            self_.num = self.num * other.den + other.num * self.den
            
        else:
            self_.num = self.num * (den/self.den) + other.num * (den/other.den)
        self_.den = den
        return self_
    
    def __sub__(self,other):
        if not isinstance(other,Fraction):
            other = Fraction(other)
        if self.num == other.num == 0:
            self.den = exprs.Expr('1')
            return self
            
        elif self.num == 0:
            return other
        elif other.num == 0:
            return self
        self_ = copy(self); st = 0
        if '/' not in format(self.den / other.den) and (not '^-' in format(self) and not '^-' in format(self.den / other.den)):
            den = self.den
        elif not '/' in format(other.den / self.den) and (not '^-' in format(other) and not '^-' in format(other.den / self.den)):
            den = other.den
        else:
            st = 1; den = self.den * other.den
        if st:
            self_.num = self.num * other.den + other.num * self.den
            
        else:
            self_.num = self.num * (den/self.den) - other.num * (den/other.den)
        self_.den = den
        return self_
    
    def __invert__(self):
        self_ = copy(self)
        self_.num = self.den
        self_.den = self.num
        return self_

    def __hash__(self):
        return hash((self.num.__hash__(),hash(self.den)))
    
    def lin_diff(self,var = 'x'):
        
        return ((self.den * self.num.lin_diff(var) - self.num * self.den.lin_diff(var))/ self.den**2).simp()

    def simp(self):
        
        return Fraction(self.num.simp(),self.den.simp())

    @property
    def struct(self):
        return [self]
        
    def __pow__(self,index):
        exchange = 0
        if isinstance(index, (int, float)) and index < 0:
            exchange = 1
            index = abs
        if index == 1:
            return self
        num = self.num ** index; den = self.den ** index
        if not num:
            return exprs.Expr('0')
        if not den:
            raise ZeroDivisionError
        
        return Fraction(exprs.Expr(str(num)) if isinstance(num,(int,
                                                                float)) else num ,
                          exprs.Expr(str(den)) if isinstance(den,(float,
                                                                  int)) else den) if exchange else Fraction(exprs.Expr(str(num)) if isinstance(num,(int,
                                                                                                                                                    float)) else num ,
                          exprs.Expr(str(den)) if isinstance(den,(float,
                                                                  int)) else den)

    def __bool__(self):
        if not self.num or not self.den:
            return False
        return True
    
    @classmethod
    def form(cls):
        return cls
    
    @property
    def recreate(self):
        return self.form()

    def __lt__(self, other):
        return format(self) < format(other)

    def __gt__(self, other):
        return format(self) > format(other)

    def __copy__(self):
        return Fraction(self.num.duplicate(),self.den.duplicate())
    def __repr__(self):
        return self.__str__()

    def __rmul__(self, other):
        return self * exprs.Expr(other)
    def __radd__(self, other):
        other = exprs.Expr(str(other))
        return self + other
    def __rsub__(self, other):
        other = exprs.Expr(str(other))
        return self - other

    def __round__(self, fix):
        return Fraction(round(self.num,fix), round(self.den, fix))
        
    

        
        
