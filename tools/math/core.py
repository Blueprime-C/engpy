from copy import copy, deepcopy
import tools.exprs as exprs
from AI import _math
from oblects.abc import (
     Utilities,
     UtilityClass,
     BaseClass,
     ExpressionObjectClass,
     BasicOperatorsClassABC
)
from misc.miscs import num, alnum, counternum, simp_var
from misc.gen import con, rev, reverse, getter
from misc.assist import (
    cd2str,
    d2lst,
    join,
    arrange_,
    m_char,
    copy,
    deepcopy,
    get_exprs
)
from misc.vars import alpha
from misc.abilities import numable, intable
from errors.exceptions import *
import math as mth

e = 2.718281828459045


class Log(BaseClass):

    def __init__(self, arg=0, base=10, coeff=1, hkeys='', s=False):
        self.s = s
        self.name = 'Log'
        if isinstance(arg, dict):
            self.expr = arg
            return
        self.base = alnum(base) if not s else 'e'
        self.coeff = alnum(coeff)
        self.arg = exprs.Expr(f"{arg}", hkeys = hkeys)

    def __str__(self):
        base = ('ln' if isinstance(self.base,
                                   float) and round(self.base,
                                                    10) == round(e,
                                                                 10) else 'log' if self.base == 10 else f"log{self.base}")
        arg = f"({self.arg})" if format(self.arg)[0] != '(' or  format(self.arg)[-1] != ')'  else f"{self.arg}"
        coeff = '' if self.coeff == 1 else self.coeff
        return f"{str(coeff)}{base}{arg}"     

    def diff(self, var):
        return ((self.coeff*self.arg.lin_diff(var))/self.arg * (1 if isinstance(self.base,
                                   float) and round(self.base,
                                                    10) == round(alnum(e),
                                                                 10) else exprs.Expr(f'log{self.base}(.e)')))

    def cal(self, values = '', desolve = True):
        arg = self.arg.cal(values,desolve = desolve) if getter(self.arg,'name') else self.arg
        coeff = self.coeff.cal(values,desolve = desolve) if getter(self.coeff,'name') else self.coeff
        base = self.base.cal(values,desolve = desolve) if getter(self.base,'name') else self.base
        try:
            return coeff * exprs.Expr(str(mth.log10(arg)/mth.log10(base)))
        except ValueError:
            raise InvalidOperation(f"log to base 10 is only valid for positive numbers: log10({arg if arg <= 0 else base})")
        except InvalidOperation:
            return log(f'{coeff}log{base}({arg})')
    
    @property
    def vars(self):
        var_list = []
        if getter(self.base, 'name'):
            var_list += self.base.vars
        if getter(self.arg, 'name'):
            var_list += self.arg.vars
        if getter(self.coeff, 'name'):
            var_list += self.coeff.vars
        return list(set(var_list))

    def __copy__(self):
        return Log(self.arg, self.base, self.coeff)

    def __deepcopy__(self):
        return Log(deepcopy(self.arg), deepcopy(self.base), deepcopy(self.coeff))

    def __hash__(self):
        return self.__str__().__hash__()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __nq__(self, other):
        return self.__hash__() != other.__hash__()

    

    __repr__ = __str__


class log(ExpressionObjectClass, UtilityClass):

    def __init__(self, expr, hkeys = '', skip=False):
        
        self.name = 'log'
        if skip or isinstance(expr, dict):
            self.expr = expr
            return
        expr = str(expr)
        expr = expr.replace(' ',
                            '').replace('##',
                                        '').replace('^-','??')
        keys = {}
        while '(' in expr:
            keys_ = m_char('#', len(keys) + 3)
            keys[keys_] = get_exprs(expr, expr.index('('))[0]
            expr = expr.replace(keys[keys_], keys_)
            
        expr = expr.replace('ln', 'loge')
        if '+' in expr:
            part = expr.split('+')
            tie = 0
            if not part[0] or part[0] == ' ':
                for key, value in reverse(keys).items():
                    part[1] = part[1].replace(key, value)
                expr = log(part[1])
                tie = 1

            else:
                for key, value in reverse(keys).items():
                    part[0] = part[0].replace(key, value)
                expr = log(part[0])

            for num, alg in enumerate(part):
                if num - 1 < tie:
                    continue
                for key, value in reverse(keys).items():
                    alg = alg.replace(key, value)
                expr += alg

            self.expr = expr.expr
            return

        if '-' in expr:
            part = expr.split('-')
            tie = 0
            if not part[0] or part[0] == ' ':
                for key, value in reverse(keys).items():
                    part[1] = part[1].replace(key, value)
                expr = log(f";{part[1]}")
                tie = 1

            else:
                for key, value in reverse(keys).items():
                    part[0] = part[0].replace(key, value)
                expr = log(part[0])

            for num, alg in enumerate(part):
                if num - 1 < tie:
                    continue
                for key, value in reverse(keys).items():
                    alg = alg.replace(key, value)
                expr -= alg
            self.expr = expr.expr
            return
        expr = expr.replace(';', '-').replace('%%%',
                                              '(-').replace('%%',
                                                            'n-').replace('%',
                                                                          's-').replace('??','^-')
        for key, value in reverse(keys).items():
            expr = expr.replace(key, value)
        n = 0;coeff = '';expr__ = {}
        while n < len(expr):
            if expr[n] in 'l':
                u = expr[n:n + 3] if (not expr[(n + 1)] == 'n') else (expr[n:n + 2])
                n += 3 if (not expr[(n + 1)] == 'n') else 2
                args = ''; pow_ = ''
                while True:
                    if expr[n] == '(':
                        break
                    pow_ += expr[n]
                    n += 1

                while True:
                    track = 0
                    if expr[n] == '(':
                        args, n = get_exprs(expr, n)
                        args = args[1:-1]; pow_ = pow_.replace('e','.e')
                        pow_ = '10' if not pow_ else '-1' if pow_ == '-' else pow_
                        
                        pow_ = alnum(pow_)
                        _pow_ = ''
                        
                        if n < len(expr) and expr[n] == '^':
                            n += 1
                            while n < len(expr):
                                    
                                if expr[n] == 'l':
                                    n -= 1
                                    break
                                else:
                                    _pow_ += expr[n]
                                n += 1
                        if not coeff:
                            coeff = 1
                        _pow_ = 1 if not _pow_ else -1 if _pow_ == '-' else alnum(_pow_)
                        coeff = 1 if not coeff else -1 if coeff == '-' else alnum(coeff)
                        coeff *= _pow_
                        expr__.update(eval(f'dict(zip([{u.title()}("{args}",pow_, hkeys = hkeys)],[1]))'))
                        n -= 1
                        break
                    else:
                        raise ImprobableError(f"Unknown Error: {expr}")

            else:
                coeff += expr[n]
            n += 1

        if expr__ == {}:
            expr__ = {'': 0}
        self.expr = {alnum(coeff): [expr__]}

    def __str__(self, stray=False):
        disp = ''
        for coeff in self.expr:
            if not coeff:
                continue
            coeff_ = coeff
            coeff = counternum(coeff)
            if coeff < 0:
                disp += (f" - {abs(num(coeff))}" if numable(coeff_) else (f"{coeff_}")) if coeff_ != -1 else ' - 1' if self.expr[coeff_] == [{'': 0}] else ' - '
            else:
                if disp:
                    disp = ' + '
                disp += (f"{coeff_}") if coeff_ != 1 else ' 1 ' if (coeff_ == 1) and (self.expr[coeff_] == [{'': 0}]) else ''
            for count, expr_ in enumerate(self.expr[coeff]):
                if count:
                    disp += ' - 1 ' if ((f"{coeff_}") if coeff < 0 else ' + {coeff_}' if coeff > 0 else coeff == -1) and (self.expr[coeff_] == [{'': 0}] or self.expr[coeff_][count] == {'': 0}) else ' + 1' if (coeff == 1) and (self.expr[coeff] == [{'': 0}] or self.expr[coeff][count] == {'': 0}) else ' - ' if coeff == -1 else f" - {abs(num(coeff))}" if numable(coeff_) else f" - {coeff}" if coeff < 0 else f" + {coeff}" if coeff > 0 else ' + '
                for var in expr_:
                    disp += (f"{var}") if var else str(abs(coeff)) if (not disp) else ''
                    if expr_[var] not in (1,0):
                        disp += f"^{expr_[var]}"
                if stray:
                    disp += '#'

        return disp if disp else '0'

    def __add__(self, other):
        self_ = deepcopy(self)
        if isinstance(other, (str, float, int)):
            other = log((f"{other}"))
        if len(other) > 1:
            for expr in other.struct:
                self_ += expr
        if len(other) == 1:
            for coeff in other.expr:
                if coeff not in self_.expr:
                    self_.expr[coeff] = []
                self_.expr[coeff].append(other.expr[coeff][0])

        return self_

    def __sub__(self, other):
        self_ = copy(self)
        if isinstance(other, (str, float, int)):
            other = log((f"{other}"))
        if len(other) > 1:
            for expr in other:
                self_ -= expr
        if len(other) == 1:
            for coeff in other.expr:
                coeff *= -1
                if coeff not in self_.expr:
                    self_.expr[coeff] = []
                self_.expr[coeff].append(other.expr[(-1 * coeff)][0])

        return self_

    def __copy__(self):
        return log(copy(self.expr), True)

    def __iter__(self):
        self.iter = self.get()
        return self

    def __len__(self):
        return len([ex for ex in self])

    def get(self):
        disp = ''
        for coeff in self.expr:
            if not coeff:
                continue
            coeff_ = coeff
            coeff = counternum(coeff)
            if coeff < 0:
                disp += (f" - {abs(num(coeff))}" if numable(coeff_) else (f"{coeff_}")) if coeff_ != -1 else ' - 1' if self.expr[coeff_] == [{'': 0}] else ' - '
            else:
                if disp:
                    disp = ' + '
                disp = f'{coeff_}' if coeff < 0 else ' + {coeff_}' if coeff > 0 else ' - 1 ' if coeff == -1 and (self.expr[coeff_] == [{'':0}] or self.expr[coeff_][count] == {'':0}) else ' + 1' if coeff ==  1 and (self.expr[coeff] == [{'': 0}] or self.expr[coeff][count] == {'':0}) else f' - ' if coeff == -1 else (f' - {abs(num(coeff))}' if numable(coeff_) else f'{coeff}') if coeff < 0 else ' + ' if coeff == 1 else f' + {coeff}' if coeff > 0 else ' + '
            for count, expr_ in enumerate(self.expr[coeff]):
                if count:
                    disp = ' - 1 ' if ((f"{coeff_}") if coeff < 0 else ' + {coeff_}' if coeff > 0 else coeff == -1) and (self.expr[coeff_] == [{'': 0}] or self.expr[coeff_][count] == {'': 0}) else ' + 1' if (coeff == 1) and (self.expr[coeff] == [{'': 0}] or self.expr[coeff][count] == {'': 0}) else ' + ' if coeff == 1 else ' - ' if coeff == -1 else (f" - {abs(num(coeff))}" if numable(coeff_) else (f" - {abs(num(coeff))}") if coeff < 0 else f" + {coeff}" if coeff > 0 else ' + ')
                for var in expr_:
                    disp += (f"{var}") if var else str(abs(coeff)) if (not disp) else ''
                    if expr_[var] not in (1,0):
                            disp += f"^{expr_[var]}"
                yield disp

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            other = exprs.Expr(str(other))
        elif isinstance(other, (str, Log)):
            other = log(other)
        elif getter(other, 'name') not in ('trig', 'Expr', 'log'):
            raise KindError(f"{type(other)} is not supported")
        sef_ = {};val_ = {};_val_= []; statr = 0
        other = other.simp()
        if not other or not self:
            return log(0)
        for __exprs__ in other.struct:
            var = list(__exprs__.expr.values())[0]
            coeff = list(__exprs__.expr)[0]
            sef = {coeff__ * coeff: var_ for coeff__, var_ in self.expr.items()}
            _sef_ = log({})
            for _var in var:
                for _coeff, vars_ in sef.items():
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
                                
                        _val_.append(val_);val_ = {}

                    _sef_.expr[alnum(_coeff)] = _val_
                    _val_ = []

            if not statr:
                add = _sef_
            else:
                add += _sef_
            statr += 1

        return add.simp() if statr else log('0')

    def __next__(self):
        return next(self.iter)

    def __hash__(self):
        return self.__str__().__hash__()

    def lin_diff(self, var = ''):
        if not var:
            var = _math['working var']
        _log = exprs.Expr({})
        for terms in self.struct:
            if isinstance(terms, log):
                coeff = terms.coeff; log_expr = list(terms.expr[coeff][0])[0]
                pow_ = terms.expr[coeff][0][log_expr]
                log_expr.coeff = coeff * pow_ 
                _log += log_expr.diff(var)
        return _log.simp()

    @property
    def vars(self):
        var_list = set()
        for exprs in self.struct:
            for keys, values in exprs.expr.items():
                for value in values[0]:
                    if isinstance(value, str):
                        var_list.add(value)
                    elif getter(value, 'name'):
                        var_list = var_list.union(set(value.vars))
                    if not isinstance(values[0][value], (int, float)):
                        var_list = var_list.union(set(values[0][value].vars))

        return list(var_list)

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
                if arrange_(var_) not in res:
                    res.update({arrange_(var_): coeff})
                else:
                    res[arrange_(var_)] = coeff + res[arrange_(var_)]

        sim = ''
        for coeff, var in res.items():
            if not var or not coeff:
                continue
            if counternum(var) > 0 and sim:
                sim += '+'
            sim += str(int(var) if intable(var) else var)
            if coeff != '^0':
                sim += coeff
        return log(sim)

    def __ne__(self, other):
        if not getter(other, 'name'):
            other = log(other)
        return hash(self.simp()) != hash(other.simp())

    @property
    def variables(self):
        return self.vars

    def __bool__(self):
        return self.expr != {0: [{'': 0}]}

    def cal(self, value='', desolve = True, **values):
        var_list = self.vars
        if isinstance(value, (float, int, str)) and not values and var_list != 1:
            raise BadRequest('Operation not Understood')
        if isinstance(value, (float, int, str)) and not values and var_list == 1:
            value = {var_list[0]: value}
        if isinstance(value, dict):
            values.update(value)
        if not values:
            values = {}
            for var_ in var_list:
                values[var_] = log(input(f"{var_}? "))

        else:
            for var in var_list:
                if var not in values:
                    values[var] = ''
        stat = log({})
        for exprs in self.struct:
            for coeffs, vars_ in exprs.expr.items():
                coeffs = log(coeffs if numable(coeffs) else coeffs.cal(values))
                for vars__ in vars_[0]:
                    if isinstance(vars__, Log):
                        _vars = vars__.cal(values, desolve = desolve) ** (vars_[0][vars__] if numable(vars_[0][vars__]) else vars_[0][vars__].cal(values, desolve = desolve))
                    else:
                        _vars = 1
                    coeffs *= _vars

            stat += coeffs

        values = {}
        return stat.simp()

    def __gt__(self, other):
        return self.__str__() > other.__str__()

    def __lt__(self, other):
        return self > other

    class iter1:

        def __init__(self, expr):
            self.expr = expr.expr
            self.it = self.get()

        def get(self):
            for coeff in self.expr:
                if not coeff:
                    continue
                for expr in self.expr[coeff]:
                    yield log({coeff: [expr]})

        def __next__(self):
            return next(self.it)

        def __iter__(self):
            return self


    @property
    def varst(self):
        var = []
        for trigs in self:
            for _trigs in list(log(trigs).expr.values())[0][0]:
                var += _trigs.arg.vars

        else:
            return list(set(var))

    def _cal(self, values=''):
        return self.cal(values) if values else self

    def __truediv__(self, other):
        if numable(self):
            return exprs.Expr(self) / other
        if other.__repr__() == '0':
            raise ZeroDivisionError('Division by Zero')
        val = {}
        if isinstance(other, (str, int, float)) or getter(other, 'name'):
            other = log(str(other))
        if len(other) == 1:
            val = log({})
            for exprs_ in self.struct:
                for _coeff, _var in exprs_.expr.items():
                    for i in range(len(_var)):
                        for coeff, var in other.expr.items():
                            for var_ in var[0]:
                                try:
                                    if not exprs_.expr[_coeff][i][var_] - var[0][var_]:
                                        exprs_.expr[_coeff][i].pop(var_)
                                    else:
                                        exprs_.expr[_coeff][i][var_] -= var[0][var_]
                                except KeyError:
                                    exprs_.expr[_coeff][0][var_] = -var[i][var_]

                        val += str(log({_coeff / coeff: [exprs_.expr[_coeff][i]]}).simp())

        return val.simp()

    def __eq__(self, other):
        if not getter(other, 'name'):
            other = log(other)
        return hash(self.simp()) == hash(other.simp())

    def __pow__(self, other):
        other = alnum(other)
        if other == 1:
            return self
        self_ = copy(self)
        if isinstance(other, float) or not numable(other):
            if numable(self) and numable(other):
                return log(str(eval(f"num({self}) ** {other}")))
            return log({1: [{self: other}]})
        for interger in range(abs(other) - 1):
            self_ *= self
        return self_ if other > 0 else Expr('1') if not other else 1/self_

    @property
    def coeff(self):
        if len(self) - 1:
            raise OperationNotAllowed
        return list(self.expr)[0]

    def __rtruediv__(self, other):
        if numable(self):
            return other / exprs.Expr(self)
        self_ = deepcopy(self)
        if other == 1:
            if len(self) != 1:
                raise InvalidOperation
            it = self_.expr[list(self_.expr)[0]][0]
            for exp in it:
                self_.expr[list(self_.expr)[0]][0][exp] *= -1

        else:
            return log(other) * 1 / self
        return self_

    def __round__(self, fix):
        coeff = [round(coeff,fix) for coeff in self.expr]
        vars_ = list(self.expr.values())
        return log(dict(zip(coeff,vars_)))

    __repr__ = __str__
