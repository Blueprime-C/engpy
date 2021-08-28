from errors.exceptions import UnacceptableToken
from misc.assist import getter


def abs_(expr):
    if isinstance(expr, (int, float)):
        return abs(expr)
    elif getter(expr, 'name'):
        return sum([-terms if terms._coeff < 0 else terms for terms in expr.struct])
    else:
        raise UnacceptableToken
