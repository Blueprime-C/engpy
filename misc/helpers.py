import tools.exprs as Ex
import tools.math.core as core
import tools.math.trigs as trigs
from .gen import getter
from errors.exceptions import UnacceptableToken


def toClass(expr, hkeys = ''):
    if 'log' in expr or 'ln' in expr:
        return core.log(expr, hkeys = hkeys)
    elif 'sin' in expr or 'sec' in expr or 'cos' in expr or 'cosec' in expr or 'tan' in expr or 'cot' in expr:
        return trigs.trig(expr, hkeys = hkeys)


def cross(cls, _cls):
    if getter(cls, 'name') == 'Expr':
        return cls
    elif getter(cls, 'name') == 'Fraction':
        return _cls({1: [{cls: 1}]})
    elif getter(cls, 'name') == 'Vector':
        return _cls(cls.vec)
    else:
        new = []
        for struct in cls.struct:
            for coeff, var in struct.expr.items():
                new.append(_cls({coeff: [{cls.recreate({1: var}): 1}]}))
        return sum(new)


def Mul(_list):
    if not isinstance(_list, (list, tuple)):
        raise UnacceptableToken(f'parameter must be a list object not {type(_list)}')
    mul_ = Ex.Expr(1)
    for items in _list:
        mul_ *= items
    return mul_