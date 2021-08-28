from fractions import Fraction


def whole(lst):
    from fundamentals.primary import Num
    den = Num(*[Fraction(lsts).limit_denominator().denominator for lsts in lst]).LCM()
    return [lsts * den for lsts in lst]


def con(dic):
    res = ''
    for key, value in dic.items():
        res += f'({key})^{value}' if not isinstance(key,str) and value != 1 else f'{key}' if value == 1  else f'{key}^{value}'
    return res


def _con(dic):
    res = ''
    for key, value in dic.items():
        res += f'{key}^{value}#' if value != 1 else f'{key}'
    return res


def con_(dic, sep='##'):
    res = ''
    for key, value in dic.items():
        if isinstance(key,str):
            return con(dic)
        res += f'{key}'.replace(sep,str(value).replace(' ',''))
    return res

def dict_uncommon(x,y):
    dict_1 = {k: v for k, v in x.items() if k not in y or y[k] != v}
    dict_1.update({k: v for k, v in y.items() if k not in x or x[k] != v})

    return dict_1


def com_arrays(x,y):
    
    """This Function return x intersection y"""
     
    return [var for var in x if var in y]


def com_arr_str(x,y):

    """This Function return (x intersection y) U ('[',']',',',"'",' ')` """
    
    return [var for var in x if var in y and not var in ('[',']',',',"'",' ')]


def rev(d):
    return {values: keys for keys, values in d.items()}


def reverse(d):
    keys = list(d);keys.reverse()
    values = list(d.values()); values.reverse()
    return dict(zip(keys,values))


def startwith(s, a = 1):
    s = str(s)
    n = 0
    while n < len(s) and not s[n].isalpha():
        n += 1
    try:
        return s[n:n + a]
    except IndexError:
        return ''


def start_alpha_index(s):
    i = 0; s_ = 0
    for i, j in enumerate(str(s)):
        if j.isalpha():
            s_ = 1
            break
    return i if s_ else None


def getter(cls,attr):
    try:
        return getattr(cls, attr)
    except AttributeError:
        return None


def th(i, verbose = False):
    if not isinstance(i,int):
        raise TypeError(f'arg must be an Integer not {type(i)}')
    if i == 1:
        return '1st' if not verbose else 'first'
    elif i == 2:
        return '2nd' if not verbose else 'Second'
    elif i == 3:
        return '3rd' if not verbose else 'third'
    else:
        return f'{i} + th'


def check_rest(list_, string):
    for lists in list_:
        if lists in string:
            return True
    return False


def dstar(d):
    return ', '.join([f'{key} = {value}' for key, value in d.items()])


def star(d):
    return ', '.join([f'{value}' for value in d])


def imap(*iterables):
    iterables = [iter(iterable) for iterable in iterables]
    while True:
        next_ = []; _next = None
        for iterable in iterables:
            try:
                g = next(iterable)
            except StopIteration:
                g = None
            if _next is None and g is not None:
                _next = True
            next_.append(g)
        if _next:
            yield next_
        else:
            break

