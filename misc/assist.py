
import copy as cy
from .miscs import num, counternum
from .vars import alpha, greek_map
from .gen import startwith, con_, _con, getter, rev
from .abilities import numable
from errors.exceptions import *
from concurrent


def wrap(char,char_space):
    string = ''; char = str(char)
    string = m_char(' ',((char_space-len(char))//2) + (char_space-len(char)) % 2)
    string += char
    string += m_char(' ',(char_space-len(char))//2)
    if len(string) < char_space:
        string += ' '
    return string


def m_char(char,times = 1):
    char_ = ''
    for i in range(times):
        char_ += char
    return char_


def once():
    return '  %/--\n#\/ x'


class pr_rt:
    def __init__(self,num,s = False):
        if s:
            self.form = num
            return 
        num = str(num)
        self.form = once().replace('x',num).replace('--',m_char('-', len(num) + 1))

    def __str__(self):
        return self.form.replace('#','').replace('%', '')

    def __add__(self,other):
        if isinstance(other, pr_rt):
            return pr_rt(self[1] + ' ' + other[1] + self[2] + ' ' + other[2].replace('\n', ' '), True)
        else:
            return pr_rt(self[1] + ' ' + m_char(' ', len(other)) + self[2] + ' ' + other, True)

    def __radd__(self, other):
        other = str(other)
        return pr_rt(self.form.replace('#', f'#{other}').replace('%', f'%{m_char(" ", len(other))}'), True)

    def __getitem__(self, index):
        if index == 1:
            return self.form[:self.form.index('\n')]
        elif index == 2:
            return self.form[self.form.index('\n'):]


def d2lst(D):
    string = []
    disp = ''
    for coeff in D:
        if not coeff:
            continue
        coeff_ = coeff
        coeff = counternum(coeff)
        if coeff < 0:
            disp = (f' - {abs(num(coeff))}' if numable(coeff_) else f'{coeff_}') if coeff_ != -1 else ' - 1' if D[coeff_] == [{'':0}] else ' - '
        else:
            if string:
                disp = ' + '
            disp += f'{coeff_}' if coeff_ != 1 else ' 1 ' if coeff_ == 1 and D[coeff_] == [{'':0}] else ''
        for count,expr_ in enumerate(D[coeff_]):
            if count:
                disp = f'{coeff_}' if coeff < 0 else f' + {coeff_}' if coeff > 0 and not coeff == 1 else ' - 1 ' if coeff == -1 and (D[coeff_] == [{'':0}] or D[coeff_][count] == {'':0}) else ' + 1' if coeff ==  1 and (D[coeff] == [{'': 0}] or D[coeff][count] == {'':0}) else f' - ' if coeff == -1 else (f' - {abs(num(coeff))}' if numable(coeff_) else f'{coeff}') if coeff < 0 else ' + ' if coeff == 1 else f' + {coeff}' if coeff > 0 else ' + '
            for var in expr_:
                if not var:
                    continue
                pw = ''
                if expr_[var] != 1 and expr_[var] != 0:
                    pw += '-' if expr_[var] == -1 else f"{expr_[var]}"
                disp += f'({var})^{pw}' if '##' not in str(var) else f'{var}'.replace('##',pw).replace('sin-','cosec').replace('cos-','sec').replace('tan-','cot') if var else str(abs(coeff)) if not disp else ''
            string.append(disp)
    return string if string else ['0']


def cd2str(cls):
    return ''.join(d2lst(cls.expr))


def join(d1, d2):
    d1.update({keys : values for keys, values in d2.items()})

    return d1


def arrange(elem, stray=False):
    elem = con_(elem)
    if '^' in elem:
        return elem
    char = startwith(elem)
    coeff = elem[:elem.index(char)]
    elem_ = elem[elem.index(char):]
    elem_ = elem_.split(')')
    for count, elems in enumerate(copy(elem_)):
        elem_[count] = elems + ')' if '(' in elems else elems
    _elem_ = []
    for alphas in alpha:
        for elems in elem_:
            if startwith(elems) == alphas:
                _elem_.append(elems)
    _elem_.sort()
    return (coeff + ''.join(_elem_)).replace('cos(0)','')


def arrange_(elem):
    elem = _con(elem)
    char = startwith(elem)
    coeff = elem[:elem.index(char)]
    elem_ = elem[elem.index(char):]
    elem_ = elem_.split('#')
    elem_.sort()
    return coeff + ''.join(elem_) if coeff != '1' else ''.join(elem_)


def _copy(obj, deep = False):
    
    if isinstance(obj, (str, int, float)):
        return obj
    elif isinstance(obj, list):
        return [(_copy(items) if not deep else deepcopy(items)) for items in obj]
    elif isinstance(obj, set):
        return {(_copy(items) if not deep else deepcopy(items)) for items in obj}
    elif isinstance(obj, dict):
        return {(_copy(keys) if not deep else deepcopy(keys)): (_copy(values) if not deep else deepcopy(values)) for keys, values in obj.items()}
    elif getter(obj, 'name') in ('Expr', 'Fraction', 'log', 'trig', 'tan'):
        return copy(obj)
    elif getter(obj, 'name') in ('sin', 'cos'):
        return deepcopy(obj)
    elif getter(obj, 'name') == 'Log':
        return obj.__copy__()
    

def refract(d):
    d_ = {}
    for keys, values in d.items():
        if '>' in keys:
            d_.update({keys:values})
    for keys, values in d.items():
        if '>' not in keys:
            d_.update({keys:values})
    return d_


def copy(obj):
    if getter(obj, 'name') in ('sin', 'cos'):
        return deepcopy(obj)
    
    return (getter(obj,'recreate')(_copy(obj.expr)) if getter(obj,'recreate') else _copy(obj.expr)) if getter(obj,'recreate') else _copy(obj)


def deepcopy(obj, skip = ''):
    if not getter(obj,'name'):
        return _copy(obj, deep = True)
    if getter(obj,'name') == 'Log':
        return obj.__deepcopy__()
    new_obj = getter(obj,'recreate')({})
    for attr, values in vars(obj).items():
        if skip and ((isinstance(skip, str) and attr == skip) or ( not isinstance(skip, str) and attr in skip)):
            continue
        setattr(new_obj,attr,deepcopy(values))
    return new_obj


def get_exprs(exprs, step  = 0):
    brac = 0;_brac = 0; _step = step
    while step < len(exprs):
        if exprs[step] == '(':
            brac += 1; _brac += 1
        elif exprs[step] == ')':
            brac -= 1
        if _brac and not brac:
            break
        step += 1
    return exprs[_step:step+1], step + 1


def rev_get_exprs(exprs, step = -1, rev = True):
    brac = 0;_brac = 0; _step = step
    while step > 0 or step < -len(exprs):
        if exprs[step] == '(':
            brac -= 1
        elif exprs[step] == ')':
            brac += 1; _brac += 1
        if _brac and not brac:
            break
        step -= 1
        
    if rev:
        exprs = list(exprs[step+1: _step]); exprs.reverse()
        return ''.join(exprs), step - 1
    else:
        return exprs
    

def get_coeff(exprs,step):
    coeff = ''
    while step > 0:
        if exprs[step] == ')':
            coeff += rev_get_exprs(exprs, step, rev = False)
        if exprs[step] in ('-', '+'):
            if '-' in coeff:
                pass
            

def gk_en(alp):
    return rev(greek_map)[alp]
    

class Dict:
    def __init__(self,dic):
        if not isinstance(dic,(dict,list)):
            raise UnacceptableToken
        self.dic = dic
    def __hash__(self):
        return self.dic.__str__().__hash__()
    def __eq__(self,other):
        return hash(self) == hash(other)
    def __repr__(self):
        return str(self.dic)
    @property
    def list(self):
        return [[keys, values] for keys, values in self.dic.items()]


class List(list):
    @property
    def unique(self):
        start = self[0]
        for items in self:
            if items != start:
                return False
        return True

    
def mul(_list):
    if not isinstance(_list, (list, tuple)):
        raise UnacceptableToken(f'parameter must be a list object not {type(_list)}')
    mul_ = 1
    for items in _list:
        mul_ *= items
    return mul_


class Misc:
    def __init__(self, arg):
        self.arg = arg

    def __contains__(self,arg):
        if isinstance(arg, (list,tuple)):
            return bool(['2' for args in arg if args in self.arg])


def match_curly(string):
    start = string.index('{')
    match = []; sub = ''
    for s in string:
        if s == '{':
            sub += s
        elif s == '}':
            match.append(sub[1:])
            sub = ''
        elif sub:
            sub += s
    return match


def get_den(exprs):
    if getter(exprs, 'name') == 'Fraction':
        return [exprs.den]
    den_list = {}
    for expr in exprs.struct:
        var_list = expr.expr[expr._coeff][0]
        for var, pows in var_list.items():
            if pows < 0 or '/' in str(var):
                if '/' in format(var):
                    try:
                        var = list(list(var.expr.values())[0][0])[0].den
                    except UnacceptableToken:
                        var = var.den
                    except AttributeError:
                        den_list.update({var_: pows for var_ in get_den(var)})
                if not var in den_list:
                    var = exprs.recreate(var) if isinstance(var,str) else var
                    den_list[var] = abs(pows)
                else:
                    if abs(pows) > den_list[var]:
                        den_list[var] = abs(pows)
    return [keys**values for keys, values in den_list.items()]
 

def get_num(exprs):
    if getter(exprs, 'name') == 'Fraction':
        return [exprs.num]
    den_list = {}
    for expr in exprs.struct:
        var_list = expr.expr[expr._coeff][0]
        for var, pows in var_list.items():
            if '/' in str(var):
                try:
                    var = list(list(var.expr.values())[0][0])[0].den
                except UnacceptableToken:
                    var = var.num
                if not var in den_list:
                    den_list[var] = pows
                
    return [keys**values for keys, values in den_list.items()]


def factor_out(expr, factor=1):
    constant, gcd = factor.__extract__
    factors, new_exprs, create = {}, expr.recreate({}), expr.recreate
    for gcds, powers in gcd.items():
        if len(gcds) == 1:
            constant *= (create(gcds) if isinstance(gcds, str) else gcds) ** powers
        elif len(gcds) > 1:
            factors.update({gcds: powers})
    for exprs in expr.struct:
        coeff_, terms = exprs.__extract__
        divisor = 1
        for gcds, powers in factors.items():
            if gcds in terms:
                cleared = True
            elif -gcds in terms:
                coeff_, gcds, cleared = coeff_ * (-1) ** powers, -gcds, True
            if cleared:
                power = terms[gcds] - powers
                if not power: terms.pop(gcds)
                elif power > 0: terms[gcds] = power
                elif power < 0: divisor *= gcds ** powers
            else:
                divisor *= gcds ** powers
        new_exprs += (create({coeff_: [terms]}) / constant) / divisor
    return new_exprs


def num_mul(*nums):
    nums = sorted(list(nums), reverse=True)
    sus = {}; i = 0
    if List(nums).unique: return None, None
    while i in range(len(nums)):
        if not i: i += 1;continue
        f = -nums[i] + nums[i-1]
        if f in sus: sus[f] += 1
        else:sus[f] = 1
        i += 1
    sus_1, sus_2 = list(sus), list(sus.values())
    return sus_1[sus_2.index(max(sus_2))], max(sus_2) + 1


def replacer(string, *sub_strings):

    for strings in sub_strings:
        string = string.replace(strings, '')

    return string

