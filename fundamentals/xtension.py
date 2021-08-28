from .primary import Num
from misc.assist import getter, mul, copy
from errors.exceptions import UnacceptableToken, OperationNotAllowed


def efactors(exprs):
    from engpy.misc.helpers import cross
    if getter(exprs, 'name') != 'Expr':
        raise UnacceptableToken(f'Expr Objs are expected not {type(exprs)}')
    if len(exprs) > 1:
        raise OperationNotAllowed
    expr = exprs.recreate
    coeff, var = exprs.__extract__
    efactor = [coeff]
    for var_, pow_ in var.items():
        if isinstance(var_, str):
            efactor.append(expr(var_) ** pow_)
        else:
            efactor.append(cross(var_, expr) ** pow_)
    return efactor


def Dfactors(exprs, coeff=True):
    from engpy.misc.helpers import cross
    if getter(exprs, 'name') != 'Expr':
        raise UnacceptableToken(f'Expr Objs are expected not {type(exprs)}')
    if len(exprs) > 1:
        raise OperationNotAllowed
    expr = exprs.recreate
    coef, var = exprs.__extract__
    efactor = {coef: 1} if coeff else {}
    for var_, pow_ in var.items():
        if isinstance(var_, str):
            efactor[expr(var_)] = pow_
        else:
            efactor[cross(var_, expr)] = pow_
    return (coef, efactor) if not coeff else efactor


def EGCD(*exprs):
    if len(exprs) == 1: return exprs[0]
    egcd, nums = [], []
    for exprs_ in exprs:
        coeff, factored = Dfactors(exprs_, 0)
        nums.append(coeff)
        egcd.append(factored)
    start = egcd[0]
    for nn, factors in enumerate(egcd):
        if not nn: continue
        check, factored_dict, start_, cleared, r_start = False, {}, {}, False, {}
        for factor, power in factors.items():
            if factor in start:
                cleared = True
            elif -factor in start:
                nums[nn], factor, cleared = - nums[nn], -factor, True
            if cleared:
                check = True
                if start[factor] > power:
                    factored_dict[factor], start[factor] = power, power
                else:
                    factored_dict[factor] = start[factor]
            cleared = False
        if not check:
            return exprs_.recreate(Num(*nums).GCD())

        for factor, power in start.items():
            if factor in factored_dict:
                if len(format(factor)) == 1:
                    start_.update({format(factor): power})
                else:
                    start_.update({factor: power})
                r_start[factor] = power
        start = r_start; r_start = {}
    return exprs_.recreate({Num(*nums).GCD(): [{var: pows for var, pows in start.items()}]})



