import tools.math as math
import tools.exprs as exprs
from misc.miscs import num,alnum,counternum
from AI import _math
from oblects.abc import Utilities, UtilityClass
from oblects.abc import ExpressionObjectClass
from oblects.abc import BasicOperatorsClassABC
from misc.gen import con_,rev, reverse,getter
from misc.assist import cd2str, d2lst,join,arrange,m_char
from misc.assist import copy,deepcopy,get_exprs
from misc.miscs import simp_var
from misc.vars import alpha
from misc.abilities import numable,intable
from errors.exceptions import *


class cos:
    def __init__(self,arg = 90,coeff = '1', arc = '', h = False, hkeys = ''):
        self.name = 'cos'
        self.h = 'h' if h else ''
        self.arc = 'arc' if arc else ''
        if isinstance(arg,dict):
            self.expr = arg
            return
        self.expr = {alnum(coeff):[exprs.Expr(str(arg), hkeys = hkeys)]}
        
    def __str__(self):
        disp = '';sin = ''
        for count, (coeff, trig) in enumerate(self.expr.items()):
            
            if coeff.__str__().replace(' ','')[0] != '-':
                sin = ' + '
            for count, _trig in enumerate(trig):
                if count: 
                    disp += sin
                disp += f'{str(coeff)}{self.arc}cos{self.h}##({_trig})'if coeff != -1 and coeff != 1 else f'{str(coeff).replace("1","")}{self.arc}cos{self.h}##({_trig})'
        return disp

        
    def __add__(self,other):
        self_ = copy(self)
        if not isinstance(other,cos):
            other = cos(0,other)
        for coeff, _cos in other.expr.items():
            if coeff in self_.expr:
                self_.expr[coeff] += _cos
            else: self_.expr[coeff] = _cos
        return self_
    
    def diff_(self,var):
        
        return trig(f'tan({self.args})')*self.args.lin_diff(var)*self.coeff*trig(f'sec({self.args})')

    def diff(self,var):
        return trig(f'sin({self.args})')*self.args.lin_diff(var)*-self.coeff

    def cal(self,values = '', desolve = True):
        arc = 'a' if self.arc else ''

        try:
            val = exprs.Expr(str(eval(f'list(self.expr)[0] * math.{arc}cos{self.h}(self.args._cal(values, desolved = desolve))')), skip = desolve)
            return val if desolve else val.inroots
        except Exception:
            return trig(f'{list(self.expr)[0]}{self.arc}cos{self.h}({self.args._cal(values)})')
        
    def laplace(self,in_var, out_var):
        return exprs.Expr(f'{out_var}/({out_var}^2 {"-" if self.h else "+"} ({self.args.coeff(in_var)})^2)')

    def ztransform(self, in_var, out_var):
        return exprs.Expr(f'{out_var}^2 - {out_var}cos{self.h}({self.args.coeff(in_var)})')/exprs.Expr(f'{out_var}^2 - 2{out_var}cos{self.h}({self.args.coeff(in_var)}) + 1')

    def in_exp(self):
        
        return exprs.Expr(f'e^(j({self.args})) + e^(-j({self.args}))')/2

    def __copy__(self):
        return cos(self.expr)
    @property
    def args(self):
        return self.expr[list(self.expr)[0]][0]
    @property
    def vars(self):
        return self.args.vars
    @property
    def coeff(self):
        return list(self.expr)[0]
    def __hash__(self):
        return self.__str__().__hash__()
    
    def __eq__(self,other):
        return self.__hash__() == other.__hash__()
    
    @classmethod
    def form(cls):
        return cls
    @property
    def recreate(self):
        return self.form()

    __repr__ = __str__


class sin:
    def __init__(self,arg = 90,coeff = '1', arc = '', h = False, hkeys = ''):
        self.name = 'sin'
        self.h = 'h' if h else ''
        self.arc = 'arc' if arc else ''
        if isinstance(arg,dict):
            self.expr = arg
            return
        self.expr = {alnum(coeff):[exprs.Expr(str(arg), hkeys = hkeys)]}

    def __str__(self):
        disp = '';sin = ''
        for count, (coeff, trigs) in enumerate(self.expr.items()):
            
            if coeff.__str__().replace(' ','')[0] != '-':
                sin = ' + '
            for count, _trig in enumerate(trigs):
                if count:
                    disp += sin
                disp += f'{str(coeff)}{self.arc}sin{self.h}##({_trig})' if coeff != -1 and coeff != 1 else f'{str(coeff).replace("1","")}{self.arc}sin{self.h}##({_trig})'
        return disp
        
    def __add__(self,other):
        self_ = copy(self)
        if not isinstance(other,sin):
            other = sin(90,other)
        for coeff, _cos in other.expr.items():
            if coeff in self_.expr:
                self_.expr[coeff] += _cos
            else: self_.expr[coeff] = _cos
        return self_
    
    def diff_(self,var):
        return trig(f'cot({self.args})')*self.args.lin_diff(var)*-self.coeff*trig(f'cosec({self.args})')

    def diff(self,var):
        return trig(f'cos({self.args})')*self.args.lin_diff(var)*self.coeff
    

    def cal(self,values = '', desolve = True):
        arc = 'a' if self.arc else ''
        try:
            val = exprs.Expr(str(eval(f'list(self.expr)[0] * math.{arc}sin{self.h}(self.args._cal(values, desolved = desolve))')), skip = desolve)
            return val if desolve else val.inroots
        except Exception:
            return trig(f'{list(self.expr)[0]}{self.arc}sin{self.h}({self.args._cal(values)})')

    def copy(self,trig):
        return cos(self.expr)

    def laplace(self,in_var, out_var):
        return exprs.Expr(f'({self.args.coeff(in_var)})/({out_var}^2 {"-" if self.h else "+"} ({self.args.coeff(in_var)})^2)')

    def ztransform(self, in_var, out_var):
        return exprs.Expr(f'{out_var}sin{self.h}({self.args.coeff(in_var)})')/exprs.Expr(f'{out_var}^2 - 2{out_var}cos{self.h}({self.args.coeff(in_var)}) + 1')

    def hilbert_tansform(self, in_var, out_var):
        return cos(self.args)

    def in_exp(self):
        return exprs.Expr(f'e^(j({self.args})) - e^(-j({self.args}))')/2
    
    @property
    def args(self):
        return self.expr[list(self.expr)[0]][0]
    @property
    def coeff(self):
        return list(self.expr)[0]
    @property
    def vars(self):
        return self.args.vars

    def __hash__(self):
        return self.__str__().__hash__()
    
    def __eq__(self,other):
        return self.__hash__() == other.__hash__()
    
    @classmethod
    def form(cls):
        return cls
    @property
    def recreate(self):
        return self.form()

    __repr__ = __str__


class tan:
    def __init__(self,arg = 90,coeff = '1', arc = '', h = False, hkeys = ''):
        self.name = 'tan'
        self.h = 'h' if h else ''
        self.arc = 'arc' if arc else ''
        if isinstance(arg,dict):
            self.expr = arg
            return
        self.expr = {alnum(coeff):[exprs.Expr(str(arg), hkeys = hkeys)]}

    def __str__(self):
        disp = '';sin = ''
        for count, (coeff, trig) in enumerate(self.expr.items()):
            
            if coeff.__str__().replace(' ','')[0] != '-':
                sin = ' + '
            for count, _trig in enumerate(trig):
                if count:
                    disp += sin
                disp += f'{str(coeff)}{self.arc}tan{self.h}##({_trig})' if coeff != -1 and coeff != 1 else f'{str(coeff).replace("1","")}{self.arc}tan{self.h}##({_trig})'
        return disp
        
    def __add__(self,other):
        self_ = copy(self)
        if not isinstance(other,cos):
            other = tan(45,other)
        for coeff, _cos in other.expr.items():
            if coeff in self_.expr:
                self_.expr[coeff] += _cos
            else: self_.expr[coeff] = _cos
        return self_

    def diff_(self,var):
        return trig(f'sin-({self.args})')*self.args.lin_diff(var)*-self.coeff*trig(f'cosec({self.args})')

    def diff(self,var):
        return trig(f'sec2({self.args})')*self.args.lin_diff(var)*self.coeff
    

    def cal(self,values = '', desolve = True):
        arc = 'a' if self.arc else ''
        try:
            val = exprs.Expr(str(eval(f'list(self.expr)[0] * math.{arc}tan{self.h}(self.args._cal(values, desolved = desolve))')), skip = desolve)
            return val if desolve else val.inroots
        except Exception:
            return trig(f'{list(self.expr)[0]}{self.arc}tan{self.h}({self.args._cal(values)})')
    def __hash__(self):
        return self.__str__().__hash__()
    
    @property
    def args(self):
        return self.expr[list(self.expr)[0]][0]
    @property
    def vars(self):
        return self.args.vars
    @property
    def coeff(self):
        return list(self.expr)[0]
    def __eq__(self,other):
        return self.__hash__() == other.__hash__()
    
    @classmethod
    def form(cls):
        return cls
    @property
    def recreate(self):
        return self.form()

    __repr__ = __str__
    

class trig(ExpressionObjectClass, UtilityClass):
    def __init__(self,expr,skip = False, keys = '', hkeys = ''):
        self.name = 'trig'
        if skip or isinstance(expr,dict):
            self.expr = expr
            return
        if isinstance(expr, trig):
            self.expr = expr
            return
        keys = {} if not keys else keys
        expr = str(expr)
        expr = expr.replace(' ','').replace('##','').replace('e-','&')
        expr = expr.replace('cosec-','sin').replace('sec-','cos').replace('cot-','tan')
        expr = expr.replace('sin-','cosec').replace('cos-','sec').replace('tan-','cot')

        for keys_, values in keys.items():
            expr = expr.replace(values,keys_)
        
        while '(' in expr:
            keys_ = m_char('#',len(keys) + 3)
            keys[keys_] = get_exprs(expr,expr.index('('))[0]
            expr = expr.replace(keys[keys_],keys_)
            
        if '+' in expr:
            part = expr.split('+')
            tie = 0
            if not part[0] or part[0] == ' ':
                for key, value in reverse(keys).items():
                    part[1] = part[1].replace(key,value)
                expr = trig(part[1],keys = keys)
                tie = 1
            else:
                for key, value in reverse(keys).items():
                    part[0] = part[0].replace(key,value)
                expr = trig(part[0],keys = keys)
            for num_, alg in enumerate(part):
                if num_-1 < tie:
                    continue
                for key, value in reverse(keys).items():
                    alg = alg.replace(key,value)
                expr += alg
            self.expr = expr.expr
            return
        if '-' in expr:
            part = expr.split('-');tie = 0
            if not part[0] or part[0] == ' ':
                for key, value in reverse(keys).items():
                    part[1] = part[1].replace(key,value)
                expr = trig(f';{part[1]}',keys = keys)
                tie = 1
            else:
                for key, value in reverse(keys).items():
                    part[0] = part[0].replace(key,value)
                expr = trig(part[0],keys = keys)
            for num_, alg in enumerate(part):
                if num_-1 < tie:
                    continue
                for key, value in reverse(keys).items():
                    alg = alg.replace(key,value)
                expr -= alg
            self.expr = expr.expr
            return None
        expr = expr.replace('cosec','sin-').replace('sec','cos-').replace('cot','tan-')
        for key, value in reverse(keys).items():
            expr = expr.replace(key,value)
        expr = expr.replace(';','-').replace('%%%','(-').replace('%%','n-').replace('%','s-')
        expr = expr.replace('&', 'e-')
        n = 0;coeff = '';expr__ = {}
        while n < len(expr):
            h = False
            if expr[n] in ('a', 's','c','t'):
                if expr[n] == 'a':
                    u = expr[n+3:n+6]
                    arc = True; n += 3
                else:
                    u = expr[n:n+3]
                    arc = False
                n += 3
                if expr[n] == 'h':
                    h = True; n += 1
                args = '';pow_ = ''
                while True:
                    if expr[n] == '(':
                        break
                    pow_ += expr[n]
                    n+= 1
                while True:
                    track = 0
                    if expr[n] == '(':
                        args, n = get_exprs(expr,n)
                        args = args[1:-1]
                        pow_ = '1' if not pow_ else '-1' if pow_ == '-' else pow_
                        pow_ =  alnum(pow_)
                        
                        expr__.update(eval(f'dict(zip([{u}("{args}", h = {h}, arc = {arc}, hkeys = hkeys)],[pow_]))'))
                        
                        n -= 1
                        break
                    raise ImprobableError(f'Unknown Error: {expr}')
            else:
                coeff += expr[n]
            n += 1
        if expr__ == {}:
            expr__ = {'':0}
        if not coeff:
            coeff = '1'
        self.expr = {alnum(coeff) : [expr__]}
    

    def __str__(self):
        return cd2str(self)
    __repr__ = __str__

    def __len__(self):
        return len(d2lst(self.expr))
    
        
    def __add__(self,other):
        self_ = deepcopy(self)
        if isinstance(other,(str, float, int,cos,sin,tan)):
            other = trig(f'{other}')
        elif getter(other,'name') == 'Expr':
            return other + self
        ## check duplicates
        if len(other) > 1:
            for expr in other:
                self_ += expr
        if len(other) == 1:
            for coeff in other.expr:
                if coeff not in self_.expr:
                    self_.expr[coeff] = []
                self_.expr[coeff].append(other.expr[coeff][0])
        return self_

    def laplace(self, in_var, out_var):
        res = exprs.Expr({})
        for expr in self.struct:
            coeff = expr.coeff
            var = expr.expr[coeff][0]
            if len(var) > 1 and pow_ > 1:
                raise InvalidOperation
            var_ = list(var)[0]; pow_ = var[var_]
            res += coeff *var_.laplace(in_var, out_var)

        return res

    def in_exp(self):
        res = exprs.Expr({})
        for trigs in self.struct:
            coef = trigs.coeff
            _var = list(trigs.expr[coef][0])[0]
            pow_ = trigs.expr[coef][0][_var]
            if isinstance(_var,(cos,sin)):
                res += coef * _var.in_exp() ** pow_
            else:
                res += coef * _var ** pow_
                
        return res
            
    def ztransform(self,in_var, out_var):
        res = exprs.Expr({})
        for expr in self.struct:
            coeff = expr.coeff
            var = expr.expr[coeff][0]
            if len(var) > 1 and pow_ > 1:
                raise InvalidOperation
            var_ = list(var)[0]; pow_ = var[var_]
            res += coeff *var_.ztransform(in_var, out_var)

        return res
            

    def __sub__(self,other):
        self_ = deepcopy(self)
        if isinstance(other,(str, float, int,cos,sin,tan)):
            other = trig(f'{other}')
        
        ## check duplicates
        if len(other) > 1:
            for expr in other:
                self_ -= expr
        if len(other) == 1:
            for coeff in other.expr:
                coeff *= -1
                if coeff not in self_.expr:
                    self_.expr[coeff] = []
                self_.expr[coeff].append(other.expr[-1*coeff][0])
        return self_


    def __mul__(self,other):
        if isinstance(other,(int,float, set)) or numable(str(other)):# Ensuring that we are dealing with Expr or trig object
            skip = False
            if isinstance(other,set):
                other = list(other)[0]; skip = True
            if not getter(other, 'name') == 'Expr':
                other = exprs.Expr(format(other), skip  =  skip)
            if numable(self):
                return other * self
        elif isinstance(other,(str,cos,sin,tan)):
            other = trig(other)
        elif not other.name in ('trig','Expr'):
            raise KindError(f'{type(other)} is not supported')
        sef_ = {};val_ = {};_val_= []; statr = 0
        other = other.simp()
        if not other or not self:
            return trig(0)
        for __exprs__ in other.struct:
            var = list(__exprs__.expr.values())[0]
            coeff = list(__exprs__.expr)[0]
            sef = {coeff__* coeff : var_ for coeff__, var_ in self.expr.items()}
            sef_ = trig(sef)
            _sef_ = trig({})
            for _var in var:
                for _coeff, vars_ in sef_.expr.items():
                    for vars__ in vars_:
                        for _vars__ in vars__:
                            if _vars__ in _var:
                                val_[_vars__] = vars__[_vars__] + _var[_vars__]
                                    
                            else:
                                val_[_vars__] = vars__[_vars__]
                            for __vars__ in _var:
                                if __vars__ not in val_:
                                    val_[__vars__] = _var[__vars__]
                        for item in copy(val_):
                            if not val_[item]:
                                val_.pop(item)
                        
                        _val_.append(val_);val_ = {};
                    _sef_.expr[int(_coeff) if intable(_coeff) else _coeff] = _val_
                    _val_ = []
            if not statr:
                add = _sef_
            else:
                add += _sef_
            statr += 1
        return add.simp() if statr else trig('0')

    def  __eq__(self,other):

        if isinstance(other, str) and len(other) < 6:
            return False
        if not getter(other,'name') == 'trig':
            other = trig(other)
        return hash(self.simp()) == hash(other.simp())
    
    def __iter__(self):
        self.n = 0
        self.list = d2lst(self.expr)
        return self
    
    def __copy__(self):
        return trig(deepcopy(self.expr))

    def __rmul__(self,other):
        return self * other
    
    def __hash__(self):
        return self.__str__().__hash__()

    def cal(self,value = '', desolve = True, **values):
        var_list = self.vars
        if isinstance(value,(float,int,str)) and not values and len(var_list) != 1:
            raise BadRequest('Operation not Understood')
        if isinstance(value,(float,int,str)) and not values and var_list == 1:
            value = {var_list[0]: value}
        if isinstance(value,dict):
            values.update(value)
        if not values:
            values = {}
            for var_ in var_list:
                values[var_] = trig((input(f'{var_}? ')))
        else:
            for var in var_list:
                if not var in values:
                    values[var] = ''
                
        stat = trig({})
        for exprs_ in self.struct:
            for coeffs, vars_ in exprs_.expr.items():
                coeffs = trig(coeffs if numable(coeffs) else coeffs.cal(values))
                for vars__ in vars_[0]:
                    if not isinstance(vars__,str):
                        _vars = vars__.cal(values, desolve = desolve) ** ({(vars_[0][vars__] if numable(vars_[0][vars__]) else vars_[0][vars__].cal(values,
                                            desolve = desolve))} if desolve else (vars_[0][vars__] if numable(vars_[0][vars__]) else vars_[0][vars__].cal(values,
                                            desolve = desolve)))                 
                    else:
                         _vars = 1
                    
                    coeffs *= _vars
                    
            stat += coeffs
            
        return stat.simp()

    def  __ne__(self,other):
        if not getter(other,'name'):
            other = trig(other)
        return hash(self.simp()) != hash(other.simp())
    
    def __bool__(self):
        return self.expr != {0:[{'':0}]}
    
    
    def _cal(self,values = ''):
        return self.cal(values) if values else self

    def ceal(self, values = ''):
        if not values:
            values= {}
        self_ = bind(self)
        f = exprs.Expr(self_[0],1).cal(join(values,rev(self_[1])))
        return f if numable else trig(f.__str__())
    
    def lin_diff(self,var = ''):
        if not var:
            var = _math['working var']
        _trig = trig({},1)
        for trigs in self.struct:
            coeff = trigs.coeff
            trigs_ = trigs.expr[coeff][0]
            if not len(trigs_) - 1:
                _trigs_ = trig({(coeff if numable(coeff) else 1):[trigs_]})
                coef = _trigs_.coeff; _var = list(_trigs_.expr[coef][0])[0]; pow_ = _trigs_.expr[coef][0][_var]
                prime = _var.diff(var) if pow_ > 0 else _var.diff_(var); coef_ = prime.coeff; var_ = prime.expr[coef_][0]
                xmul = -1 if pow_ < 0 else 1
                _trig__ = trig({coef*abs(pow_):[{_var:xmul *(abs(pow_)-1)}]}) * prime
                _trig += _trig__ * coeff + _trigs_ * coeff.lin_diff(var) if not numable(coeff) else _trig__
                
            else:
                __trig_ = trig({})
                for i in range(len(trigs_)):
                    current = {}; rem = {}
                    for count, (key, values) in enumerate(trigs_.items()):
                        if count == i:
                            current = {key:values}
                        else:
                            rem.update({key:values})
                        __trig_ += trig({1:[current]}).lin_diff(var) * trig({1:[rem]})
                _trig += __trig_ * coeff + trig({1:[trigs_]}) * coeff.lin_diff(var) if not numable(coeff) else coeff * __trig_

        return _trig.simp()
    
    def simp(self):
        if self.expr in ({0: [{'': 0}]}, {0: [{}]}):
            return trig(0)
        res = {}
        for coeff, var in self.expr.items():
            if not coeff:
                continue
            if var == [{}]:
                var = [{'': 0}]
            for var_ in var:
                if not arrange(var_) in res:
                    res.update({arrange(var_):coeff})
                else:
                    res[arrange(var_)] = coeff + res[arrange(var_)]
        sim = ''
        for coeff, var in res.items():
            if not var or not coeff:
                continue
            if counternum(var) > 0 and sim:
                sim += '+'
            sim += str(int(var) if intable(var) else var)
            if coeff != '^0':
                sim += coeff
                
        return trig(sim)

    def __gt__(self,other):
        return self.__str__() > other.__str__()

    def __lt__(self,other):
        return self > other

    @property
    def vars(self):
        var_list = set()
        for exprs_ in self.struct:
            for keys,values in exprs_.expr.items():
                for value in values[0]:
                    if isinstance(value, str):
                        var_list.add(value)
                    elif getter(value,'name'):
                        var_list = var_list.union(set(value.vars))
                    if not isinstance(values[0][value],(int,float)):
                        var_list = var_list.union(set(values[0][value].vars))
                        
        return list(var_list)

    def __pow__(self,other):
        other = alnum(other)
        if other == 1:
            return self
        self_ = copy(self)
        if isinstance(other,float) or not numable(other):
            if numable(self) and numable(other):
                return trig(str(eval(f'num({self}) ** {other}')))
            else:
                coeff = self.coeff; arg = self.expr[coeff][0]; arg[list(arg)[0]] *= other
                return trig({coeff: [arg]})
        for interger in range(abs(other)-1):
            self_ *= self
        return self_ if other > 0 else Expr('1') if not other else 1/self_

        
    def __next__(self):
        if self.n == len(self.list):
            raise StopIteration
        next_ = self.list[self.n]
        self.n += 1
        q = 0
        while q < len(next_):
            if next_[q].isalnum():
                break
            elif next_[q] == '+':
                q += 2
                break
            elif next_[q] == '-':
                q = 0
                break
            q += 1
        return next_[q:]

    @property
    def unit(self):
        self_ = copy(self)
        coeff = self.coeff
        var = self.expr[coeff][0]
        if len(var) > 1:
            raise OperationNotAllowed
        var_ = list(var)[0]
        self_.expr[coeff][0][var_] = 1
        return self_

    @property
    def pow(self):
        coeff = self.coeff
        var = self.expr[coeff][0]
        if len(var) > 1:
            raise OperationNotAllowed
        return list(var.values())[0]

    @property
    def coeff(self):
        if len(self) - 1:
            raise OperationNotAllowed
        return list(self.expr)[0]

    @property
    def variables(self):
        return self.vars
    
    def __truediv__(self,other):
        if numable(self):
            return exprs.Expr(self)/other
        if other.__repr__() == '0':
            raise ZeroDivisionError('Division by Zero')
        val = {}
        if isinstance(other,(str,int,float)) or getter(other,'name'):
            other = trig(str(other))
        if len(other) == 1:
            val = trig({})
            for exprs_ in self.struct:
                for _coeff,_var in exprs_.expr.items():
                    for i in range(len(_var)):
                        for coeff, var in other.expr.items():
                            for var_ in var[0]:
                                try:
                                    if not exprs_.expr[_coeff][i][var_] -var[0][var_]:
                                        exprs_.expr[_coeff][i].pop(var_)
                                    else:
                                        exprs_.expr[_coeff][i][var_] -= var[0][var_]
                                except KeyError:
                                    exprs_.expr[_coeff][0][var_] = - var[i][var_]
                        val += str(trig({_coeff/coeff:[exprs_.expr[_coeff][i]]}).simp())
                     
        
        return val.simp()
    def __rtruediv__(self,other):
        if numable(self):
            return other/exprs.Expr(self)
        self_ = deepcopy(self)
        if other == 1:
            if len(self) != 1:
                raise InvalidOperation
            it = self_.expr[list(self_.expr)[0]][0]
            for exp in it:
                self_.expr[list(self_.expr)[0]][0][exp] *= -1
        else:
            return trig(other) * 1/self
        return self_

    def __round__(self, fix):
        coeff = [round(coeff,fix) for coeff in self.expr]
        vars_ = list(self.expr.values())
        return trig(dict(zip(coeff,vars_)))
