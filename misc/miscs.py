from . import alpha, _alpha
from .abilities import numable, counterable
from .gen import getter
from math import e
from errors.exceptions import InvalidOperation, UnacceptableToken
from errors.wreck import Fizzle


def num(num_):
    try:
        unt_num = int(float(format(num_).replace(' ', '')))
        fl_nium = float(format(num_).replace(' ', ''))
        
        return unt_num if unt_num == fl_nium else fl_nium
    except Exception:
        if getter(num_, 'name') == 'Fraction' or '/(' in format(num_):
            return 1
        raise InvalidOperation(f"You can't take the numeric value of {num_}, you can try alnum({num_})")


def simp_var():
    for var in alpha:
        if var in ['e', 'ȩ', 'î', 'ĵ', 'ǩ']:
            continue
        yield var


def simp_Var():
    for var in _alpha:
        yield var


def _isinstance(cls,obj):
    return f"<class '__main__.{obj}'>" == format(type(cls))


def numity(num):
    try:
        unt_num = int(float(format(num).replace(' ', '')))
        fl_nium = float(format(num).replace(' ', ''))
        
        return unt_num if unt_num == fl_nium else fl_nium
    except Exception:
        return None


def nums(*num_):
    return [num(num_s) for num_s in num_]


def alnums(*num_):
    
    return [alnum(num_s) for num_s in num_]


def counternum(num_):
    if counterable(num_):
        raise UnacceptableToken('Unacceptable character present')
    numl = format(num_)
    couter = ''
    for char in numl:
        if not char.isalpha():
            couter += char
        else:
            break
    return num(couter)


def alnum(al, exp=False):
    if isinstance(al, set):
        al = list(al)[0]
    elif isinstance(al, (int, float, str)) and not al:
        return 0
    if isinstance(al, str):
        if al == 'nil':
            return 'nil'
        elif al in ('e', '.e', 'ȩ'):
            return e
    if al is None:
        return None
    try:
        al = eval(al)
    except Exception:
        pass
    nmm = numity(al)
    if nmm is not None:return nmm
    if getter(al, 'name') == 'Expr':
        simp = al.desolved
        nmm = numity(simp)
        return nmm if nmm is not None else simp
    else:
        try:
            Expr
        except NameError:
            from engpy.tools.exprs import Expr
        exp = Expr(format(al)); simp = exp.desolved
        nmm = numity(simp)
        return nmm if nmm is not None else simp


def fnum(al, exp = False):
    if isinstance(al, set):
        al = list(al)[0]
    elif isinstance(al, (int, float)) and not al:
        return 0
    if isinstance(al, str):
        if al == 'nil':
            return 'nil'
        elif al in ('e', '.e', 'ȩ'):
            return e
        elif not al:
            return 0
    if al is None:
        return None
    try:
        al = eval(al)
    except Exception:
        pass
    nmm = numity(al)
    if nmm is not None:return nmm
    if getter(al, 'name') == 'Expr':
        simp = al.desolved
        nmm = numity(simp)
        if nmm:
            return nmm
        raise Fizzle(f"{al} can't be forcefully taken as a number")
    else:
        try:
            Expr
        except NameError:
            from engpy.tools.exprs import Expr
        exp = Expr(format(al)); simp = exp.desolved
        nmm = numity(simp)
        if nmm:
            return nmm
        raise Fizzle(f"{al} can't be forcefully taken as a number")


def roundnum(nums):
    nums= num(nums)
    return int(nums) + 1 if round(nums, 10) == int(nums) + 1 else nums

def lexpr(*expr):
    try:
        Expr
    except NameError:
        from engpy.tools.exprs import Expr
    return [Expr(exprs) for exprs in expr]
