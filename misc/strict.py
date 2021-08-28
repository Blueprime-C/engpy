from .miscs import simp_Var
from .gen import rev


def bind(cls, _pairs=''):
    alpha = simp_Var()
    _cls = cls.__str__()
    new = {}
    if not _pairs:
        _pairs = {}
    for key, value in cls.expr.items():
        new[key] = []
        for count, values in enumerate(value):
            new[key].append({})
            for pairs, _values in values.items():
                if not isinstance(pairs, (str, int, float)) and 'class' in str(type(pairs)):
                    if pairs in _pairs:
                        new[key][count][_pairs[pairs]] = _values
                        continue
                    while True:
                        alpha_ = next(alpha)
                        if alpha_ == 'F' or alpha_ in _pairs.values():
                            continue
                        if alpha_ not in _cls:
                            break
                    new[key][count][alpha_] = _values
                    _pairs[pairs] = alpha_
                else:
                    new[key][count][pairs] = _values

    return new, _pairs


def cast(cls, _pairs):
    new = {}
    _pairs = rev(_pairs)

    for key, value in cls.expr.items():
        new[key] = []
        for count, values in enumerate(value):
            new[key].append({})
            for pairs, _values in values.items():
                if pairs in _pairs:
                    new[key][count][_pairs[pairs]] = _values
                else:
                    new[key][count][pairs] = _values
    return new
