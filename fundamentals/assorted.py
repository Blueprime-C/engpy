from math import factorial
from misc.assist import getter
from .primary import Num


def P(n, r):
    return int(factorial(n) / factorial(n - r))


def C(n, r):
    return int(P(n, r) / factorial(r))


def GCD(*factors):
    if len(factors) == 1: return factors[0]
    from .xtension import EGCD
    for factor in factors:
        if getter(factor, 'name') == 'Expr':
            return EGCD(*factors)
    return Num(*factors).GCD()


def CD(neg=False, *factors):
    return GCD(*factors) not in (-1, 1) if neg else GCD(*factors) != 1
