from misc.gen import getter
from errors.exceptions import UnacceptableToken

def mix(exprs):
    if not isinstance(exprs,(list, tuple)):
        raise UnaccpetableToken(f'arg must be a list or tuple not {type(exprs)}')
    expr_dict = {}
    res = exprs[0].recreate({})
    for expr_ in exprs:
        for _expr in expr_:
            if _expr in expr_dict:
                expr_dict[_expr] += 1
            else:
                expr_dict[_expr] = 1
    for pairs, values in expr_dict.items():
        if values == len(exprs):
            res += pairs
    return res
