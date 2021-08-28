import AI
from fractions import Fraction
from math import *
from fundamentals.primary import Num, break_pq
from AI.settings import const, configuration
from fundamentals.secondary import pascal, group_factor, difference_powers
from fundamentals.assorted import GCD
from misc.gen import con, reverse, getter, startwith, th, com_arrays, dict_uncommon
from misc.gen import start_alpha_index, rev
from misc.gen import check_rest, dstar, imap
from errors.exceptions import *
from errors.wreck import Fizzle
from misc.assist import m_char, copy, deepcopy, get_exprs, factor_out, num_mul, replacer
from misc.assist import Dict, mul, Misc, join, get_den
from misc.assist import refract, gk_en
from misc.internals import iformat
from misc.abilities import intable, intable_, numable
from misc.scan.scan_expr import scan_MD
from misc.vars import alpha_greek as alpha
from misc.vars import greek_map, constants
from misc.vars import chars
from misc.helpers import toClass, cross, Mul
from misc.miscs import num, alnum, numity
from lib.transforms import Transforms
from oblects.abc import Utilities, UtilityClass, ExpressionObjectClass, BasicOperatorsClassABC
from oblects.cls import mix
from oblects.assist import New_Raph, modified_New_Raph
from oblects.KnowledgeBase import Article
from visuals import Visualize
from misc.utilities import Range
from tools._fractions import Fraction as Frac
import misc.helpers as help_
import random

try:
    from numpy import int32
except (ImportError, OSError) as e:
    from misc.omissions import Nothing
    int32 = Nothing

__all__ = ['Expr', 'Eqns']

complex_id = ('î', 'ĵ', 'ǩ')

alpha_ = copy(alpha)


class Expr(ExpressionObjectClass, Utilities.expr, BasicOperatorsClassABC, UtilityClass, Article, AI.Implementation):
    """               ========
                      | Expr |
                      ========
        The Base Class is for all Algebraic Manipulations
        Expr Objects are Mathematical Functions or Expressions

        The Expr class takes either a dict object or string:

        1. Strings:
            Conversion of strings to Expr Objects conforms to
            Linear Math Input. Use strings when representing
            complex or long Expressions in Expr Object

            e.g
                1. P(x) = 2x^3 + 4x^2 - 11x - 7
                    To represent this with Expr class

                    >>> from engpy.tools.exprs import Expr
                    >>> Px = Expr('2x^3 + 4x^2 - 11x - 7')

                2. F(x,y) = -3x^2y - 4xy^2 + 15xy - 4

                    To represent this with Expr class
                    >>> from engpy.tools.exprs import Expr
                    >>> Fxy = Expr('-3x^2y - 4xy^2 + 15xy - 4')

                3. F(x) = 2sin(x) + 7h^2sin(-3x)cos(x + y) - 4tan2(x^2)
                    >>> from engpy.tools.exprs import Expr
                    >>> Fx = Expr('2sin(x) + 7h^2sin(-3x)cos(x + y) - 4tan2(x^2)')

                Note:
                    1.  Space don't count when representing expressions.
                        e.g Expr('2  x  yco  s( -3x) + 5 x^ -2 + 4xy+log2(25x)')
                        is the same as Expr('2xycos(-3x) + 5x^-2 + 4xy + log2(25x)')
                    2.  When exponents are in form of product use bracket
                        e.g
                            P(s) = s^2 + s^2t + s^-2r
                            >>> from engpy.tools.exprs import Expr
                            >>> Ps = Expr('s^2 + s^(2t) + s^(-2r)')
                            because E('s^2 + s^2t + s^-2r') is the same as
                            Expr('s^2 + t * s^2 - r * s^-2') which entirely different
            Expr strings can also contain greek alphabets
            e.g
                V(t) = Vsin(ωt)
                >>> Vt = Expr('Vsin(omega t)')
                since space doesn't count this is the same as
                >>> Vt = Expr('Vsin(omegat)')

                Expr strings can also contain subscripts

                I(c) = I0 sin(ωt + π/2)
                >>> I = Expr('I0 sin(omegat + pi/2)')

                X(c) = 1/2πf0C
                >>> X = Expr('1/2pif0C')

                Z(t) = 2π/(L/C)^0.5
                >>> Zt = Expr('2pi/sqrt(L/C)')

            For common alphabet like e (exp as in 2.718281828459045) put . in front

            F(t) = exp^(-2t) + exp(2t)

            >>> Ft = Expr('.e^(-2t) + .e^(2t)')

            For complex numbers use .i, .j, .k

        2. Dict -Object
            Conversion of Dict object to Expr Objects follow this pattern

            {coefficient:list of dict-object with the same coefficients}

            NoTE: The coefficients must be either integer or float
                  The list must be list of dict-objects with variables as the keys
                  and values as the powers
            e.g
               P(x) = 2x^3 + 4x^2 - 11x - 7
               >>> Expr({2:[{'x':3}], 4:[{'x': 2}], -11:[{'x': 1}], -7:[{'':0}]})
               Note that this is the same as Expr('2x^3 + 4x^2 - 11x - 7')

               P(x,y) = 2x^3y^2 + 2xy^3 - 4x^2 - 11xy - 7
               >>> "Expr({2: [{'x': 3, 'y': 2}, [{'x': 1, 'y': 3}], -4: [{'x': 2}], -11: [{'x': 1, 'y': 1}], 7: [{'': 0}]})"
            Be careful, any mistake in the format may lead to undesired or corrupt Expression.


            However, even though using dict format with difficult and stressfull, it's much much much faster than using strings.

            But for complex expressions like, trigs, log, ln use strings
    """

    def __init__(self, expr, keys='', hkeys='', skip='', **kwargs):
        global alpha
        self.name = 'Expr'
        if getter(expr, 'Expr'):
            self.expr = expr.expr
            return
        elif isinstance(expr, set):
            skip = 1
            _expr = list(expr)[0]
            if getter(_expr, 'name') == 'Expr':
                self.expr = _expr.expr
                return
            expr = format(_expr)


        elif isinstance(expr, dict):
            self.expr = expr
            return
        elif isinstance(expr, (int, float)) or numable(expr):
            self.expr = {num(expr): [{'': 0}]}
            return
        elif isinstance(expr, complex):
            expr = str(expr).replace('j', 'ĵ')
        elif getter(expr, 'name'):
            self.expr = cross(expr, Expr).expr
            return
        if expr == '!@#$%^':
            self.expr = {}
            return
        if 'alpha' in kwargs:
            alpha = kwargs['alpha']
        shift = 0
        for char in expr:
            if ord(char) > 33000:
                shift += 1
        self.num = ''
        _rest = ['cosec', 'sec']

        step = 0
        var, coeff, pow_, initial = '', '', '', len(alpha)
        _var = {}
        _pow = []
        chk = 0
        self.expr = {}
        _expr = expr
        expr = expr.replace(' ', '').replace('^-', '@').replace('^+', '$')
        expr = expr.replace('.e', 'ȩ').replace('.i', 'î').replace('.j', 'ĵ').replace('.k', 'ǩ')
        expr = expr.replace('.F', 'Ƒ')
        expr = expr.replace('cosec-', 'sin').replace('sec-', 'cos').replace('cot-', 'tan')
        if not expr:
            expr = '0'
        safe = {}
        for rests in _rest:
            if rests in expr:
                rests_ = m_char('$', 3 + len(safe))
                safe[rests_] = rests
                expr = expr.replace(safe[rests_], rests_)
        for greeks in greek_map:
            if not greeks in ('eta', 'Eta'):
                expr = expr.replace(greeks, greek_map[greeks])
        expr = expr.replace('eta', greek_map['eta']).replace('Eta', greek_map['Eta'])
        expr = expr.replace('e-', '%')
        expr = expr.replace('e', '&')
        spec_char = {'&': '', '%': '', '!': ''}
        expr__ = expr
        sq = 0
        expr = expr.replace(')(', ')*(')
        expr = expr.replace('sin-', 'cosec').replace('cos-', 'sec').replace('tan-', 'cot')
        rest = ['log', 'cos', 'cosec', 'sec', 'tan', 'cot', 'sin', 'ln', 'cosh', 'sinh', 'tanh',
                'arc', 'arcsin', 'arccos', 'arctan']
        for key, value in reverse(safe).items():
            expr = expr.replace(key, value)
        if not keys:
            keys = {}
        if not hkeys:
            hkeys = {}
        expr = expr.replace('@', '^-').replace('$', '^+')
        while 'sqrt' in expr:  # To remove radicals
            s = expr.index('sqrt(')
            s += 4
            rad, s = get_exprs(expr, s)
            pow__ = ''
            if s < len(expr) and expr[s] == '^':
                while True:
                    s += 1
                    if s == len(expr):
                        break
                    elif expr[s] == '(':
                        radd = get_exprs(expr, s)[0]
                        pow__ += radd
                        break
                    elif expr[s] == '-':
                        if pow__:
                            break
                    elif expr[s] == '+':
                        if pow__:
                            break
                    elif expr[s] in ('*', '/', ')'):
                        break
                    pow__ += expr[s]
            pow1 = alnum(pow__) * .5 if pow__ else .5
            pow2 = f'^{pow__}' if pow__ else ''
            expr = expr.replace(f'sqrt{rad}{pow2}', f'{rad}^{pow1}')
            sq = 1

        def brack(expr='', start_pt=None, c=True, chk=chk):
            if expr.count(')') != expr.count('('):
                raise UnacceptableToken(f'Parenthesis mismatched {_expr}')
            _coeff = ''
            coeff = ''
            time = 0
            pre_expr = ''
            encap = 0
            rephase = False
            while ')' in expr:
                if pre_expr in expr:
                    if not time - 3:
                        encap = 1
                        time = 0
                        start_pt = None
                    time += 1
                pre_expr = expr

                if ')' in expr and not '(' in expr:
                    raise ImprobableError('An unknown error occured')
                # Reading coefficient of Brackets from LHS and marking the begining of the bracket
                while ')(' in expr:
                    expr = expr.replace(')(', ')#(')
                    temp_index = expr.index('#') - 1
                    restart = True
                    L_brac = ''
                    mul_list = []
                    brac = 0
                    std = temp_index + 2
                    while temp_index > -1:
                        if expr[temp_index] == ')':
                            brac += 1

                        elif expr[temp_index] == '(':
                            brac -= 1
                        if not brac:
                            L_brac += '('
                            break
                        L_brac += expr[temp_index]
                        temp_index -= 1
                    L_brac = list(L_brac)
                    L_brac.reverse()
                    L_brac = ''.join(L_brac)
                    mul_list.append(L_brac)
                    L_brac = ''
                    temp_index = std
                    while temp_index < len(expr) and restart:
                        if expr[temp_index] == '(':
                            brac += 1

                        elif expr[temp_index] == ')':
                            brac -= 1
                        if not brac:
                            if temp_index + 1 < len(expr):
                                if expr[temp_index + 1] != '#':
                                    restart = False
                            L_brac += ')'
                            break
                        L_brac += expr[temp_index]
                        temp_index += 1
                    mul_list.append(L_brac)
                    L_brac = ''

                    for hash_ in mul_list:
                        keys_ = m_char(chr(33014 + len(hkeys) + 1 + shift))
                        alpha.append(keys_)
                        chars.append(keys_)
                        hkeys[keys_] = hash_[1:-1]
                        expr = expr.replace(hash_, keys_)
                    expr = expr.replace('#', '')
                    rephase = True

                if ')^' in expr:
                    if '/(' in expr:
                        expr = div(expr, expr.index('/('))
                    expr = powers(expr)
                    continue
                if ')/' in expr:
                    expr = div(expr, expr.index(')/') + 1)
                    continue
                if '/(' in expr:
                    expr = div(expr, expr.index('/('))
                    continue

                if ')*(' in expr:
                    expr = mult(expr, expr.index(')*(') + 1)
                    continue
                if '*' in expr:
                    expr = mult(expr, expr.index('*'))
                    continue

                n = start_pt if start_pt else 0
                once = 0
                mask = 0
                sign = ''
                stat = 0
                add_sign = False
                # Reading Brackets
                while c:
                    while n < len(expr) and (expr[n].isdigit() or expr[n].isalpha() or expr[n] in ('-', '.', '^')):
                        if expr[n] in ('-', '+', '*', '/') and coeff and expr[n - 1] != '^':
                            coeff, once, mask, sign, stat = '', 0, 0, '', n
                        if not once:
                            if expr[n - 1] == '#':
                                mask = 1
                                once = 1
                        coeff += expr[n]
                        if not sign:
                            if expr[n] in ('+', '-'):
                                sign += expr[n]
                        n += 1
                    if n >= len(expr) or expr[n] == '(':
                        break
                    coeff, once, mask, sign = '', 0, 0, ''
                    n += 1
                if stat and expr[stat - 1] in ('^', '@'):
                    coeff = ''

                if expr[stat - 1] in ('+', '-'):
                    add_sign = True
                coeff_ = coeff
                if coeff == '-':
                    coeff = '-1'
                nn = 0
                __nn = n + 1
                n += 1
                _coeff = ''
                # Marks the end of the bracket
                while n < len(expr):
                    if n < len(expr) and expr[n] == '(':
                        nn += 1
                    if expr[n] == ')' and not nn:
                        break
                    elif expr[n] == ')':
                        nn -= 1
                    n += 1
                nn_ = n + 1
                command = 4 if coeff and coeff[-1] == '^' else 0
                if check_rest(rest, coeff_):
                    command = 1
                # Reading coefficient of Brackets from RHS
                while nn_ < len(expr):
                    if any([expr[nn_].isdigit(), expr[nn_] in ('.', '^'), expr[nn_].isalpha()]):
                        _coeff += expr[nn_]
                    else:
                        break
                    nn_ += 1
                if check_rest(rest, _coeff) and nn_ < len(expr) and expr[nn_] == '(':
                    _coeff = ''

                inbrac = expr[__nn:n]
                if command:
                    if not command - 4:
                        coeff_ = '^'
                    if check_rest(rest, _coeff) or mask:
                        _coeff = ''
                        chk += 1
                        keys_ = m_char(f'#{m_char(">", chk)}', len(keys) + 5 + shift)
                    else:
                        keys_ = ':' + m_char('#', len(keys) + 5 + shift) + ':'
                    if rest in Misc(_coeff):
                        _coeff = ''
                    coeff_ = coeff_[1:] if coeff_[0] == '-' else coeff_
                    keys[keys_] = f'{coeff_}({inbrac}){_coeff}'
                    expr = expr.replace(keys[keys_], keys_)
                    command = 0
                    continue
                if encap:
                    keys_ = m_char(chr(33014 + len(hkeys) + 1 + shift))
                    alpha.append(keys_)
                    chars.append(keys_)
                    hkeys[keys_] = inbrac
                    expr = expr.replace(inbrac, keys_)
                    encap = False
                    continue
                # Looking for Differentials
                if 'Ƒ' in coeff:
                    ind = coeff.index('F')
                    _var = []
                    ind += 1
                    while ind < len(coeff):
                        _var.append(coeff[ind])
                        ind += 1
                    __var = _var
                    if not _var:
                        __var = 'x'
                    vars_ = "".join(_var)
                    in_brac_expr = str(
                        Expr(coeff.replace(f'F{vars_}', '') if coeff.replace(f'F{vars_}', '') else '1') * Expr(
                            inbrac).lin_diff(__var) * Expr(_coeff if _coeff else '1'))
                else:

                    rep = ''
                    in_brac = inbrac
                    # To directly remove variable with index e.g x1
                    if rephase:
                        for char in copy(inbrac):

                            if char.isalpha() or char.isnumeric():
                                if rep and rep[-1].isalpha() and char.isnumeric():
                                    rep += char
                                elif not rep and char.isalpha():
                                    rep += char
                            else:
                                rep = ''
                            if len(rep) == 2:
                                keys_ = m_char(chr(33014 + len(hkeys) + 1 + shift))
                                alpha.append(keys_)
                                chars.append(keys_)
                                hkeys[keys_] = rep
                                inbrac = inbrac.replace(f'({rep})', keys_)
                                rephase = False

                    if all([coeff == '1' or coeff == '', _coeff == '1' or _coeff == '']):
                        in_brac_expr = Expr(inbrac)
                    else:
                        in_brac_expr = Expr(coeff if coeff else '1') * Expr(inbrac) * Expr(
                            _coeff if _coeff else '1')  # Simplifying the expression in the bracket)
                _str = iformat(in_brac_expr)
                if _str[0].isalnum() and add_sign:
                    _str = '+' + _str
                expr = expr.replace(f'{coeff_}({in_brac}){_coeff}', _str)  # Substitution in to the expr
                for i in range(len(expr)):
                    if expr[i] in ('+', '-'):
                        break
                    if expr[i].isdigit():
                        expr = '+' + expr
                        break

            return expr

        def powers(expr, n=''):

            while ')^' in expr:

                std = expr.index(')^')
                LHS = ''
                brac = 0
                sign = 0
                std_ = std + 2
                minus = False
                # Reading the expression on LHS

                while std > -1:
                    if expr[std] == ')':
                        brac += 1
                    elif expr[std] == '(':
                        brac -= 1
                    if brac <= 0 and expr[std] in ('+', '-', '(', '*'):
                        if expr[std] == '-' and minus:
                            break
                        if expr[std] in ('(', '-'):
                            LHS += expr[std]
                        if std > 0 and expr[std] == '(' and expr[std - 1] not in ('/', '+', '(', '*'):
                            if expr[std - 1] == '-':
                                minus = True
                            std -= 1
                            continue
                        else:
                            break
                    LHS += expr[std]
                    std -= 1
                LHS = list(LHS)
                LHS.reverse()
                LHS = ''.join(LHS)
                LSH = LHS

                command = 1
                if LHS[0:2] == '-(':
                    LHS = LHS.replace('-(', '-1(')
                coef = '1'
                n = 0
                # Preventing the coefficient from the index
                if '(' in LHS and LHS[0] != '(':
                    coef = ''
                    while n < len(LHS):
                        if LHS[n] != '(':
                            coef += LHS[n]
                        else:
                            LHS = ('#' + LHS).replace('#' + coef, '')
                            break

                        n += 1
                if coef[-1] == '*':
                    coef = coef[:-1]
                RHS = ''
                brac = 0
                no_brac = True
                minus = False
                cate = ''
                cate_s = False
                cates = ''
                # Reading the index
                while std_ < len(expr):
                    if expr[std_] == '(':
                        r, std_ = get_exprs(expr, std_)
                        RHS += r
                        std_ -= 1
                        break
                    if expr[std_] not in ('/', ')', '*'):
                        if expr[std_].isalpha():
                            if not cate and not cates:
                                cate = 'a'
                            else:
                                break
                        elif expr[std_].isnumeric():
                            cates = 1
                        elif expr[std_] in ('-', '+'):
                            if RHS:
                                break
                    else:
                        break
                    RHS += expr[std_]

                    std_ += 1
                for rests in rest:
                    if rests in coef:
                        keys_ = ':' + m_char('#', len(keys) + 5 + shift) + ':'
                        keys[keys_] = f'{LSH}^{RHS}'
                        expr = expr.replace(keys[keys_], keys_)
                        command = 0
                if command:

                    in_brac_expr = (Expr(LHS, keys=keys, hkeys=hkeys) ** RHS)
                    if isinstance(in_brac_expr, (int, float)):
                        in_brac_expr = Expr(str(in_brac_expr))

                    if coef != 1 and not coef == '1':
                        in_brac_expr *= coef
                    in_brac_expr = in_brac_expr.simp()

                    _str = str(in_brac_expr)

                    new_expr = _str
                    while ')^' in new_expr or '^(' in new_expr:
                        rpg = str(in_brac_expr._coeff) if in_brac_expr._coeff != 1 else ''

                        for _exprs_ in in_brac_expr.struct:
                            coeff__ = _exprs_._coeff
                            len_keys = len(hkeys)
                            exprs__ = _exprs_.expr[coeff__][0]
                            count_pow = new_expr.count(')^') + new_expr.count('^(')
                            for exprs_, _pow_ in exprs__.items():
                                t_expr = _exprs_.duplicate()
                                t_expr.expr[coeff__][0].pop(exprs_)
                                t_str = str(t_expr)
                                if count_pow != t_str.count(')^') + t_str.count('^('):
                                    break

                            __Exprs = Expr({1: [{exprs_: _pow_}]})
                            __Exprs_ = Expr({1: [{exprs_: 1}]})
                            if ')^' in str(_exprs_):
                                keys_ = m_char(chr(33014 + len(hkeys) + 1 + shift))
                                alpha.append(keys_)
                                chars.append(keys_)
                                hkeys[keys_] = exprs_
                                exprs_ = keys_

                            if '^(' in str(_exprs_):
                                if getter(_pow_, 'name'):
                                    _keys_ = m_char(chr(33014 + len(hkeys) + 1 + shift))
                                    hkeys[_keys_] = _pow_
                                    _pow_ = _keys_
                            if len_keys == len(hkeys):
                                continue
                            sign = ''  # '-' if _exprs_._coeff < 0 else ''
                            string = str(__Exprs)
                            string_ = str(__Exprs_)
                            if coeff__ and coeff__ not in ('1', 1):
                                sub_str = f'({string_})'
                                if sub_str in expr:
                                    string = string.replace(string_, sub_str)

                            new_expr = new_expr.replace(string, f'{sign}{exprs_}^{_pow_}')

                        expr = expr.replace(f'{LSH}^{RHS}'
                                            , new_expr).replace(rpg,
                                                                '%$#').replace(str(hkeys[exprs_])
                                                                               , exprs_).replace('%$#', rpg)

                        continue
                    if std > 0 and (expr[std] in ('*', '/') or expr[std - 1] in ('*', '/')):
                        _str = '(' + _str + ')'
                    expr = expr.replace(f'{LSH}^{RHS}', _str)

            return expr

        def div(expr, std=''):

            while '/' in expr:

                LSH, LHS, RHS, n = scan_MD(expr, '/', std)
                in_brac_expr = (Expr(LHS.replace('&', 'e'), alpha=alpha, hkeys=hkeys) / Expr(RHS.replace('&', 'e'),
                                                                                             keys=keys,
                                                                                             hkeys=hkeys)).simp()
                in_brac_exprs = iformat(in_brac_expr)
                if '/(' in in_brac_exprs and len(in_brac_expr) == 1:
                    keys_ = m_char(chr(33014 + len(hkeys) + 1 + shift))
                    alpha.append(keys_)
                    chars.append(keys_)
                    if len(in_brac_expr) == 1:
                        in_brac_expr = list(in_brac_expr.__extract__[1])[0]
                    hkeys[keys_] = in_brac_expr
                    if expr[n] in ('+', '-'):
                        keys_ = '+' + keys_
                    expr = expr.replace(f'{LSH}/{RHS}', keys_)
                elif in_brac_exprs.replace(' ', '')[0].isalnum() and not expr[n] in ('+', '-'):
                    in_brac_expr = '+' + in_brac_exprs
                if getter(in_brac_expr, 'name') != 'Fraction':
                    expr = expr.replace(f'{LSH}/{RHS}', str(in_brac_expr) if not std or expr[n] in expr[n] in (
                        '+', '-') else f'({str(in_brac_expr)})')
                if std:
                    break

            return expr

        def mult(expr, std=''):
            std__ = std
            while '*' in expr:
                in_time = 0
                mul_list = []
                expr_ = expr
                while True:
                    if not in_time:
                        LSH, LHS, RHS, n = scan_MD(expr_, '*', std, 1)
                        mul_list += [LHS, RHS]
                    else:

                        if n > len(expr_) - 1 or not expr_[n + 1:] or expr_[n] != '*':
                            break
                        expr_ = expr_[n + 1:]
                        LHS, RHS, n = scan_MD(expr_, state='2')[1:]
                        mul_list += [LHS, RHS]
                    if mul_list[-1] is None or not mul_list[-1]:
                        del mul_list[-1]
                        break

                    in_time += 1
                if mul_list[-1].count(')') > mul_list[-1].count('('):
                    mul_list[-1] = mul_list[-1][:-1]
                std = std__
                LSH, LHS, RHS, n = scan_MD(expr, '*', std)
                mul_list_ = copy(mul_list)
                mul_list_[0] = Expr(mul_list_[0])
                in_brac_expr = mul(mul_list_)

                if getter(in_brac_expr, 'name') == 'Fraction':
                    keys_ = m_char(chr(33014 + len(hkeys) + 1 + shift))
                    alpha.append(keys_)
                    chars.append(keys_)
                    hkeys[keys_] = in_brac_expr
                    expr = expr.replace('*'.join(mul_list), keys_)
                elif iformat(in_brac_expr)[0].isalnum() and not expr[n] in ('+', '-'):
                    in_brac_expr = '+' + iformat(in_brac_expr)
                if getter(in_brac_expr, 'name') != 'Fraction':
                    expr = expr.replace('*'.join(mul_list), str(in_brac_expr))
                if std:
                    break

            return expr

        expr = brack(expr)

        expr = div(expr)
        expr = mult(expr)

        expr = brack(expr)

        sig_count = 0
        n_expr = copy(expr)
        expr = ''
        # To fix multiple sign; e.g -----, --++--
        while sig_count < len(n_expr):
            sig_res = 1
            dis = 0
            while sig_count < len(n_expr) and n_expr[sig_count] in ('+', '-', ' '):
                sig_res *= eval(n_expr[sig_count] + '1')
                sig_count += 1
                dis = 1
            expr += ('+' if sig_res > 0 else '-') if dis else ''
            expr += n_expr[sig_count] if sig_count < len(n_expr) else ''
            sig_count += 1
            dis = 0

        del n_expr
        del sig_count
        del sig_res
        expr = expr.replace('^-', '@')
        expr = expr.replace('e-', '%')
        if '+' in expr:
            part = expr.split('+')
            tie = 0
            if not part[0] or part[0] == ' ':
                expr = Expr(part[1], keys=keys, hkeys=hkeys)
                tie = 1
            else:

                expr = Expr(part[0], keys=keys, hkeys=hkeys)
            for _num, alg in enumerate(part):
                if _num - 1 < tie:
                    continue

                for key, value in refract(reverse(keys)).items():
                    alg = alg.replace(key, value)
                hkey_ = 0
                for keys_ in hkeys:
                    if keys_ in alg:
                        hkey_ = 1
                        break

                expr += (alg, hkeys) if hkey_ else alg
            self.expr = expr.expr
            return
        if '-' in expr:
            part = expr.split('-')
            tie = 0
            if not part[0] or part[0] == ' ':
                expr = Expr({f';{part[1]}'}, keys=keys, hkeys=hkeys)
                tie = 1
            else:
                expr = Expr(part[0], keys=keys, hkeys=hkeys)

            for _num, alg in enumerate(part):
                if _num - 1 < tie:
                    continue
                for key, value in refract(reverse(keys)).items():
                    alg = alg.replace(key, value)
                hkey_ = 0
                for keys_ in hkeys:
                    if keys_ in alg:
                        hkey_ = 1
                        break

                expr -= (alg, hkeys) if hkey_ else {alg} if skip else alg
            self.expr = expr.expr
            return None

        for key, value in refract(reverse(keys)).items():
            expr = expr.replace(key, value)

        expr = expr.replace(';', '-').replace('@', '^-').replace('$', '^+').replace('?', 'e^')

        # Serializing expressions into Dict
        while True:
            _pow = ''
            revert = ''
            to_continue = False
            while step < len(expr) and (
                    expr[step].isdigit() or expr[step] in ('+', '-', '.') or expr[step] in spec_char):
                if not coeff and expr[step] == '+':
                    step += 1
                    continue
                if expr[step] == '&' and step + 1 < len(expr) and expr[step + 1] == '^':
                    break
                coeff += expr[step]
                step += 1

            while step < len(expr) and (expr[step].isalnum() or expr[step] in ('+', '-', '^', '&', '(')):
                crossd = False
                if not to_continue:
                    var = ''
                to_continue = False
                if expr[step] != '^':
                    if expr[step] == '(':
                        revert = expr
                        expr, to_step = get_exprs(expr, step)
                        expr = expr[1:-1]
                        step = 0
                    sparse = 6

                    if sparse and '(' in expr[step:] and expr[step] in ('a', 'l', 'c', 's', 't', 'h'):
                        _var_ = ''
                        step_ = step
                        while step < len(expr) and expr[step].isalpha():
                            _var_ += expr[step]
                            step += 1
                        if _var_[:3] in rest or _var_[:5] in rest:

                            if '(' in expr[step:]:
                                var, step = get_exprs(expr, step_)

                            if _var_[:3] in ('log', 'ln'):
                                discard = 0
                                _step_ = step
                                if _step_ < len(expr) and expr[_step_] == '^':

                                    var += expr[_step_]
                                    _step_ += 1
                                    _pow = ''
                                    discard = 1
                                    while _step_ < len(expr):
                                        if expr[_step_].isdigit() or (expr[_step_] == '-' and not _pow):
                                            _pow += expr[_step_]
                                            var += expr[_step_]
                                        else:

                                            break

                                        _step_ += 1

                                    pow_ = ''
                                    step = _step_
                                var = toClass(var, hkeys=hkeys)
                                _pow = ''
                                crossd = True
                            else:
                                var = toClass(var, hkeys=hkeys)
                                crossd = True
                            step -= 1
                        else:
                            step = step_
                            sparse = 0
                            var = 'e' if expr[step] == '&' else expr[step]
                    else:
                        if expr[step].isalpha():
                            var = expr if revert else 'e' if expr[step] == '&' else expr[step]
                        elif expr[step].isnumeric():
                            var += expr[step]
                        else:

                            var = expr if revert else 'e' if expr[step] == '&' else expr[step]
                        sparse = 1
                    step += 1
                if revert:
                    expr, step = revert, to_step
                try:
                    if expr[step].isnumeric() and not crossd:
                        to_continue = True
                        continue
                except IndexError:
                    pass
                try:
                    if step < len(expr) and expr[step] == '^':
                        step += 1
                        pow_ = ''
                        while step < len(expr):
                            if expr[step] == '(':
                                pow_, step = get_exprs(expr, step)

                                pow_ = alnum(pow_)
                                break
                            else:
                                if expr[step].isalpha() and pow_:
                                    break
                                pow_ += expr[step]
                            step += 1
                    else:
                        pow_ = 1
                except IndexError:
                    pass
                if var in hkeys:
                    var = hkeys[var]
                if pow_ in hkeys:
                    pow_ = hkeys[pow_]
                if len(var) - 1:
                    alpha.append(var)
                    chars.append(var)

                if pow_ != '0':
                    _var[var] = alnum(pow_)
                elif not var:
                    pow_ = ''
                    coeff = '1'

            if not _var:
                _var = {'': 0}
            if not coeff:
                coeff = 1
            elif coeff == '-':
                coeff = '-1'
            coeff = f'{coeff}'.replace("%", "e-")
            coeff = coeff.replace("&", "e") if coeff == '&' else coeff.replace("&", "*e")
            coeff = factorial(int(coeff.replace('!', ''))) if coeff[-1] == '!' else eval(coeff)

            _var_ = {}
            for var_, pows in _var.items():
                if pows and not var_:
                    if numable(pows):
                        coeff **= num(pows)
                        continue

                    else:
                        _var_[Expr(f'{abs(coeff)}')] = alnum(pows)
                        coeff = 1 if coeff > 0 else -1
                        continue
                _var_[var_] = pows
            coeff *= eval(_pow) if _pow else 1
            if coeff not in self.expr:
                self.expr[coeff] = []
            if not _var_:
                _var_ = {'': 0}
            self.expr[coeff].append(_var_)
            if step >= len(expr):
                break
        while len(alpha) != initial:
            del alpha[-1]

        if not skip:
            self.expr = self.inconsts(1).expr
        if sq:
            self.expr = self.inroots.expr

    def __str__(self, get=False, d=True, s=False):

        if d:
            self_ = self.duplicate()
            self_.expr = self_.desolved.expr
        else:
            self_ = self
        if s:
            d = True
        disp = ''
        for coeff in (self_.expr if not get == '' else get):
            disp_ = ''
            if not coeff:
                continue
            if coeff < 0:
                disp_ = f' - {abs(coeff)}' if coeff != -1 else ' - 1' if self_.expr[coeff][0] == {'': 0} else ' - '
            else:
                if disp:
                    disp_ += ' + '
                disp_ += f'{coeff}' if coeff != 1 else ' 1 ' if coeff == 1 and str(self_.expr[coeff][0]) == str(
                    {'': 0}) else ''
            for count, expr_ in enumerate(self_.expr[coeff]):
                _var__, emb, _disp, coeff_= '', 0, '', coeff
                if count:
                    disp_ = ' - 1 ' if coeff == -1 and (self_.expr[coeff] == [{'': 0}] or self_.expr[coeff][count] == {
                        '': 0}) else ' + 1' if coeff == 1 and (
                            self_.expr[coeff] == [{'': 0}] or self_.expr[coeff][count] == {
                        '': 0}) else f' - ' if coeff == -1 else f' - {abs(coeff)}' if coeff < 0 else f' + {coeff}' if coeff > 0 and coeff != 1 else ' + '
                for count_, var in enumerate(expr_):
                    _vva = format(var)
                    brac = False
                    powe = expr_[var]
                    if getter(var, 'name') == "Expr" and len(var) == 1:
                        c, v = var.__extract__
                        for i in v:
                            if numable(i) or len(v) > 1 or (c != 1 and not isinstance(powe, (int, str))):
                                brac = True
                                break
                    _var__ = f'({_vva})' if ((brac or len(var) > 1) and len(_vva) > 1) or '/' in _vva and \
                                            get_exprs(_vva)[0] != _vva else _vva if not coeff - 1 and not isinstance(
                        var, str) else f'({_vva})' if not isinstance(var, str) and expr_[var] != 1 else _vva
                    if not isinstance(var, str) and len(var) == 1:
                        if getter(var, 'name') == 'Expr':
                            if var._coeff - 1 and not numable(var) and isinstance(powe, (int, str)):
                                c, va = var.__extract__
                                coeff_ *= c ** powe
                                emb = 1
                                _var__ = Expr({1: [va]})
                                _vva = format(_var__)
                                _var__ = f'({_vva})' if ((brac or len(var) > 1) and len(var) > 1) or '/' in _vva and \
                                                        get_exprs(_vva)[
                                                            0] != _vva else _vva if not coeff_ - 1 and not isinstance(
                                    var, str) else f'({_vva})' if not isinstance(var, str) and expr_[var] != 1 else _vva

                                _coeff_ = ' - ' if coeff_ == -1 else f' - {abs(coeff_)}' if coeff_ < 0 else '' if coeff_ == 1 else f'{coeff_}'

                        else:
                            if var.coeff - 1:
                                coeff_ *= var.coeff
                                emb = 1

                                _coeff_ = ' - ' if coeff_ == -1 else f' - {abs(coeff_)}' if coeff_ < 0 else '' if coeff_ == 1 else f'{coeff_}'

                                _var__ = _var__[start_alpha_index(_var__):]
                    if var and powe != 1:

                        pow_ = f"{expr_[var]}"
                        if not d and pow_.endswith('.5'):
                            pow_ = alnum(alnum(pow_) * 2)
                            pow_ = '' if pow_ == 1 else '^' + str(pow_) if len(str(pow_)) == 1 or numable(
                                pow_) else f'^({pow_})'
                            if _var__[0] == '(' and _var__[-1] == ')':
                                _var__ = _var__[1:-1]
                            _var__ = f'sqrt({_var__})' + pow_
                        else:
                            pow_ = '^' + pow_ if len(pow_) == 1 or numable(pow_) else f'^({pow_})'
                            _var__ += pow_
                    _disp += _var__
                disp += ((f'{_coeff_}' if not str(coeff_).replace(' ', '')[
                    0].isalnum() else f' + {_coeff_}') if emb else disp_) + _disp
        if not disp:
            return '0'
        return disp

    @property
    def tied(self):
        return self.tie

    @tied.setter
    def tied(self, value):
        self.tie = value

    def __len__(self):

        return len([1 for expressions in self.struct])

    def __add__(self, other):

        """ Addition of Expr Objects
            ========================

            Addition can happen btwn 2 Expr Objects, if the other party is not
            an Expr Object, it will be converted

            e.g
                >>> Px = Expr('2x^3 - 2x')
                >>> T = Expr('3xcos(theta)')
                >>> PTx = Px + T

                This may be written in a line
                >>> PTx = Expr('2x^3 - 2x') + Expr('3xcos(theta)')
                which is the same as
                >>> PTx = Expr('2x^3 - 2x') + '3xcos(theta)'
        """

        self_ = deepcopy(self)
        if isinstance(other, (str, float, int)):
            other = Expr(f'{other}')
        elif isinstance(other, tuple):
            other = Expr(f'{other[0]}', hkeys=other[1])
        elif isinstance(other, set):
            other = Expr(other)
        frac = 1 if getter(other, 'name') == 'Fraction' else 0
        ## check duplicates
        if not frac and len(other) > 1:
            for expr in other.struct:
                self_ += expr
        if frac or len(other) == 1:
            for coeff in other.expr:
                if frac:
                    coeff = 1
                if coeff not in self_.expr:
                    self_.expr[coeff] = []
                if frac:
                    self_.expr[coeff].append({other: 1})
                else:
                    self_.expr[coeff].append(other.expr[coeff][0])
        return self_

    def __sub__(self, other, option=''):

        """ Subtraction of Expr Objects
            ========================

            Subtraction are supported btwn 2 Expr Objects, if the other party is not
            an Expr Object, it will be converted

            e.g
                >>> Px = Expr('2x^3 - 2x')
                >>> T = Expr('3xcos(theta)')
                >>> PTx = Px - T

                This may be written in a line
                >>> PTx = Expr('2x^3 - 2x') - Expr('3xcos(theta)')
                which is the same as
                >>> PTx = Expr('2x^3 - 2x') - '3xcos(theta)'
        """

        try:
            self_ = deepcopy(self)
            if isinstance(other, (str, float, int)):
                other = Expr(f'{other}')
            elif isinstance(other, tuple):
                other = Expr(f'{other[0]}', hkeys=other[1])
            elif isinstance(other, set):
                other = Expr(other)
            ## check duplicates
            frac = 1 if getter(other, 'name') == 'Fraction' else 0

            if not frac and len(other) > 1:
                for expr in other.struct:
                    self_ -= expr
            if frac or len(other) == 1:
                for coeff in other.expr:
                    if frac:
                        coeff = 1
                    coeff *= -1
                    if coeff not in self_.expr:
                        self_.expr[coeff] = []
                    if frac:
                        self_.expr[coeff].append({other: 1})
                    else:
                        self_.expr[coeff].append(other.expr[-1 * coeff][0])
        except RuntimeError:
            self_ = self.new

        return self_

    def add(self, other, option=''):
        return self.__add__(other, option)

    def sub(self, other, option=''):
        return self.__sub__(other, option)

    def cal(self, value='', desolve=False, desolved=False, **values):

        """Expr Objects support substitution

            S(t) = ut + 0.5at^2; To calculate S(t) when u = 0, t = 4, a = 9.8

            Three options are available
            1. Bulding the values into a Python dictionary

                >>> from engpy.tools.exprs import Expr
                >>> St = Expr('ut + .5at^2')
                >>> s = St.cal({'u': 0, 't': 4, 'a': 9.8})
              Note: Using this approach all variables must convert to strings

            2. Using the = sign
                Note that Expr calculates angles in radians by default, if the
                angles is in degrees add deg to the string
                y = xtan(θ) - gx^2sec2(θ)/2u^2
                find y when x = 20, θ = 32.29, u = 30, g = 9.8

                >>> y = Expr('xtan(θ) +- gx^2sec2(θ)/2u^2')
                >>> y.cal( x = 20, theta = '33.29deg', u = 30, g = 9.8)

            3. if the expressions only has one unknown, no specification is needed
                 y = x^3 - 6x^2 + 12x - 8; find y when x = 6.2

                 >>> y = Expr('x^3 - 6x^2 + 12x - 8')
                 >>> y.cal(6.2)

            You combine both option 1 and option 2


            Note that all values in strings are converted to Expr Objects, which
            means you can also put/nest an Expr Object into another

            e.g
                if f(x) = 3x + 1 and g(x) = 2x - 1, and h(x) = x^2

                find fog, hof

                >>> fx = Expr('3x + 1')
                >>> gx = Expr('2x - 1')
                >>> fog = fx.cal(gx)

                Which can also be done as

                >>> fx = Expr('3x + 1')
                >>> fog = fx.cal('2x - 1')

                >>> hx = Expr('x^2')
                >>> hof = hx.cal('3x + 1')

            4. if you want to enter the values in real-time, just call cal
                >>> fx.cal()
                 as such cal method will iterate all the variables and prompt you
                 to enter the values, just press enter straight up to skip any variable
                 which has no value

            y = z^2 - 2xzcos(α), simplify when x = -15, α = π/6
            >>> y = Expr('z^2 - 2xzcos(alpha)')
            >>> y.cal(x = -15, alpha = 'pi/6')
            This will yield z^2 + 15sqrt(3)z
            Note that since z is not given, so we still have z after simplifying

            To request for the value at runtime we use
            >>> y.cal()
            this will prompt you to enter the values, since z is not given, just
            skip it by hitting enter.



        """
        var_list = self.vars
        const_list = self.constants
        if value and (isinstance(value, (float, int, str)) or getter(value, 'name') == 'Expr') and not values and len(
                var_list) != 1 and not desolve:
            raise Vague('Operation not Understood')
        if value and not isinstance(value, dict) and not values and len(var_list) == 1:
            value = {var_list[0]: value}
        if isinstance(value, dict):
            values.update(value)
        _desolve = any((desolve, desolved))
        if not _desolve and not values:
            values = {}
            for var_ in var_list:
                values[var_] = Expr(input(f'{var_}? '))
        else:
            for var in var_list:
                if not var in values:
                    values[var] = var
            for var in values:
                if isinstance(values[var], str):
                    values[var] = values[var].replace('deg', '* pi /180')

        desolve_ = desolved if desolved else desolve
        if _desolve:
            values.update({constant: constants[constant] for constant in self.constants})
        if self._iscomplex:
            values.update({'î': 'î', 'ĵ': 'ĵ', 'ǩ': 'ǩ'})

        values.update({greek_map[keys]: values for keys, values in copy(values).items() if keys in greek_map})
        stat = self.new
        for exprs in self.struct:
            for coeffs, vars_ in exprs.expr.items():
                coeffs = Expr({str(coeffs)})
                for vars__ in vars_[0]:
                    if getter(vars__, 'name') == 'trig':
                        desolve = desolved
                    else:
                        desolve = desolve_

                    if not isinstance(vars__, str):
                        _var = vars__.cal(values, desolve=desolve) ** (
                            {(vars_[0][vars__] if isinstance(vars_[0][vars__],
                                                             (int,
                                                              float)) else vars_[0][vars__].cal(values,
                                                                                                desolve=desolve))} if _desolve else (
                                vars_[0][vars__] if isinstance(vars_[0][vars__],
                                                               (int,
                                                                float)) else vars_[0][vars__].cal(values,
                                                                                                  desolve=desolve)))


                    elif vars__.isnumeric() or (vars__ in const_list and not isinstance(vars_[0][vars__],
                                                                                        (int, float))) or (
                            vars__ and values[vars__]) or (vars__ and values[vars__] == 0):
                        if not _desolve and vars__ in const_list and not isinstance(vars_[0][vars__], (int, float)):
                            values.update({vars__: vars__})
                        _var = (Expr(vars__, skip=_desolve) if vars__.isnumeric() else Expr(str(values[vars__]),
                                                                                            skip=_desolve) if isinstance(
                            values[vars__],
                            str) or isinstance(values[vars__],
                                               (int
                                                , float)) and values[vars__] < 0 and format(vars_[0][vars__]).endswith(
                            '.5') else values[vars__]) ** (
                                   1 if vars__.isnumeric() else {(vars_[0][vars__] if isinstance(vars_[0][vars__],
                                                                                                 (int,
                                                                                                  float)) else vars_[0][
                                       vars__].cal(values,
                                                   desolve=desolve))} if _desolve and not isinstance(values[vars__], (
                                       int, float)) else (vars_[0][vars__] if isinstance(vars_[0][vars__],
                                                                                         (int,
                                                                                          float)) else vars_[0][
                                       vars__].cal(
                                       values,
                                       desolve=desolve)))

                    elif vars__:

                        _var = f'{vars__}^{vars_[0][vars__]}'
                    else:
                        _var = 1
                    coeffs *= {_var}

            stat += {coeffs}
        return stat.desolve.simp(desolve=False) if desolve and self.variables else stat.simp(desolve=False)

    @property
    def desolve(self):

        """
            To convert all constants to their respective values
            A = πr^2
            >>> A = Expr('pir^2')
            >>> A.desolve
            This will result to 3126535r^2/995207

        """
        return self._cal(desolve=True) if self.constants else self


    def power_list(self, grouping=True):
        power = []
        for exprs in self.struct:
            coeff, var = exprs.__extract__
            power += [tuple(var.values())] if grouping else list(var.values())
        return power

    @property
    def desolved(self):
        """
            To convert all constants and radicals to their respective values
            X = tan(π/6) + π^2 + sqrt(7)
            >>> X = Expr('tan(π/6) + π^2 + sqrt(7) ')
            >>> X.desolve
            This will result to 8651503/660788

        """
        return self._cal(desolve=True)

    def _cal(self, value='', desolve=False, desolved=False, simp=True, **values):

        """
            Using _cal method safe call cal, if no values are given, the Expr
            Object will be returned instead of prompting you to enter the
            values

            Use _cal when you are not sure if a value will be given
        """

        try:
            return self.cal(value, desolve, desolved, **values) if value or values else self.cal(desolve=desolve,
                                                                                                 desolved=desolved) if any(
                [desolved, desolve]) else self.simp() if simp else self
        except ZeroDivisionError:
            return 'nil'

    def __radd__(self, other):
        return self + other

    # Sum of differentials
    def diffs(self, res='', **kwargs):
        """
            Partial Derivatives with some constant
            if F(x) = x^2 - y^2, Find  îF'(x) - ĵF'(y)

            >>> Fx = Expr('x^2 - y^2')
            >>> Fx.diffs(x = '.i', y = '.j')
            or
            >>> Fx.diffs({'x': '.i', 'y': '.j'})
        """
        if not res:
            res = {'x': 1, 'y': 1, 'z': 1}
        if not isinstance(res, dict):
            raise UnacceptableToken('Only Python Dictionaries are allowed')
        res.update(kwargs)
        return sum([f'{coef}.F{res_}' * self for res_, coef in res.items()]).simp()

    def inconsts(self, strict=False):
        """
            Re-writing Expr Objects in form of constants
            Making strict True means you are strictly substituting constants
        """
        S = self.duplicate()
        for consts in constants:
            S = S.inconst(consts, strict)

        return S

    def inconst(self, constant, strict=False):
        value = constants[constant]
        S = self.new
        for exprs in self.struct:
            coeff = exprs._coeff
            if type(coeff) == type(value) or not strict:
                c = Fraction(str(coeff / value)).limit_denominator()
                if strict and len(str(c.denominator)) > 3:
                    S += {exprs}
                else:
                    vars_ = exprs.expr[coeff][0]

                    if constant in vars_:
                        vars_[constant] += 1
                    else:
                        vars_[constant] = 1

                    S += {Expr({coeff / value: [vars_]})}
            else:
                S += {exprs}
        return S

    @property
    def in_pi(self):
        """
            Re-writing in form of π strictly
            ExprObj.in_pi
        """
        return self.inconst(chr(960), 1)

    @property
    def to_pi(self):
        """
            Re-writing in terms of π strictly
            ExprObj.inconsts
        """

        return self.inconst(chr(960))

    @property
    def inradicals(self):
        """
            Re-writing in terms of roots of prime numbers
            ExprObj.inradicals
        """
        S = self.duplicate()
        radic = Num(0).next_prime()
        while True:
            radical = next(radic)
            if radical > 100:
                break
            S = S.rephrase(radical, radical ** .5)
        return S

    @property
    def inroots(self):
        """
            Re-writing in terms of roots of numbers
            ExprObj.inroots
        """
        S = self.duplicate()
        radical = 1
        while True:
            radical += 1
            if intable(radical ** .5):
                continue
            if radical > 100:
                break
            S = S.rephrase(radical, radical ** .5)

        return S

    def rephrase(self, constant, value):
        S = self.new
        for exprs in self.struct:
            coeff = exprs._coeff
            if len(str(round(coeff, 5))) < 5 or not (isinstance(coeff, float) and len(str(coeff)) > 5):
                S += exprs
                continue
            c = Fraction(str(coeff / value)).limit_denominator()
            if len(str(c.denominator)) > 3:
                S += exprs
            else:
                vars_ = exprs.expr[coeff][0]

                if constant in vars_:
                    continue
                vars_[Expr(f'{constant}')] = 1 / 2
                if '' in vars_:
                    vars_.pop('')
                S += Expr({coeff / value: [vars_]})

        return S

    def lin_diff(self, var_='t', repeat=1, *args, **kwargs):
        """Linear Differentiation

            Differentiating Expr Objects in respect to var_

            if y = 1/(x^2 + 4) find dy/dx

            >>> y = Expr('1/(x^2 + 4)')
            >>> dydx = y.lin_diff('x')

            This will result to ( - 2x/(x^4 + 8x^2 + 16))


            if u = θcos(θ)/(θ + 3), find f'(θ)

            >>> u = Expr('thetacos(theta)/(theta + 3)')
            >>> du = u.lin_diff('theta')

            This will result to ((3cos(θ) - θ^2sin(θ) - 3θsin(θ))/(θ^2 + 6θ + 9))


            For higher derivatives add the repeat argument

            if  y = tan(θ), find f''(θ)

            >>> y = Expr('tan(theta)')
            >>> f2 = y.lin_diff('theta', 2)

            This will result to 2sec2(θ)tan(θ)


            If some calcalation are to be made on the differential, extra arguments
            can be provided which will call the cal method automatically

            Find the gradient of tangent to the curve y = x^2/(x^2 + 1) at the point
            with abscissa 1.

            These means we find the differential and then put x =  1

            >>> y = Expr('x^2/(x^2 + 1)')
            >>> dy = y.lin_diff('x')
            >>> grad = dy.cal(1)

            grad result to 1/2

            However, we can make lin_diff method to cal itself with some extra arguments
            the format is ExprObj.lin_diff(var, repeat, extra_arguments)

            So we can  solve the above question as
            >>> y = Expr('x^2/(x^2 + 1)')
            >>> grad = y.lin_diff('x', 1, 1)

            grad is still 1/2

            if f(x) = 3a^2x^3 - 4abx^2 + 16a^2bx - 12, find the gradient of the tangent
            to the tangent of f(x) at x = -3 when a = -5, b = 3

            >>> fx = Expr('3a^2x^3 - 4abx^2 + 16a^2bx - 12')
            >>> grad = fx.lin_diff('x',2, x = -3, a = -5, b = 3)

            grad = -1,230

        """
        if not self:
            return Expr('')
        if not var_:
            var_ = AI._math['working var']
        elif var_ in greek_map:
            var_ = greek_map[var_]
        if isinstance(var_, list):
            self_ = copy(self)
            for var in var_:
                self_ = self_.lin_diff(var)
            return self_
        _expr = self.new
        for exprs in self.struct:
            coeff, exprs_ = exprs.__extract__
            if not len(exprs_) - 1:
                _var = list(exprs_)[0]
                _pow = exprs_[_var]
                if isinstance(_var, str):
                    if _var == chr(553):
                        _expr += exprs * Expr(format(_pow)).lin_diff(var_)
                    elif not isinstance(_pow, (int, float)):
                        _expr += (_pow * f'ln({_var})').lin_diff(var_) * exprs

                    elif _var == var_:
                        _expr += Expr({coeff * _pow: [{_var: _pow - 1}]})
                    else:
                        _expr += Expr('')
                else:
                    if len(_var) == 1 and not isinstance(_pow, (int, float)):
                        coeff_, _var_ex = _var.__extract__
                        if coeff_ != 1 and _var_ex == {'': 0}:
                            _expr += (_pow * f'ln({coeff_})').lin_diff(var_) * exprs
                        elif len(_var_ex) > 1:
                            conv_exp = {Expr(coeff_): _pow} if coeff_ != 1 else {}
                            conv_exp.update({key: value * _pow for key, value in _var_ex.items()})
                            _expr += Expr({coeff: [conv_exp]}).lin_diff(var_).rindex()
                        else:
                            _expr += exprs * (_pow * f'ln({_var})').lin_diff(var_) if not isinstance(_pow,
                                                                                                     (int,
                                                                                                      float)) else _var.lin_diff(
                                var_) * Expr({coeff * _pow: [{_var: _pow - 1}]}) if getter(_var,
                                                                                           'name') == 'Expr' else coeff * cross(
                                (_var ** _pow).lin_diff(var_),
                                self.recreate)

                    else:
                        _expr += exprs * (_pow * f'ln({_var})').lin_diff(var_) if not isinstance(_pow,
                                                                                                 (int,
                                                                                                  float)) else _var.lin_diff(
                            var_) * Expr({coeff * _pow: [{_var: _pow - 1}]}) if getter(_var,
                                                                                       'name') == 'Expr' else coeff * cross(
                            (_var ** _pow).lin_diff(var_),
                            self.recreate)

            else:
                __exprs_ = Expr({})
                for i in range(len(exprs_)):
                    current = {}
                    rem = {}
                    for count, (key, values) in enumerate(exprs_.items()):
                        if count == i:
                            current = {key: values}
                        else:
                            rem.update({key: values})
                    __exprs_ += Expr({1: [current]}).lin_diff(var_) * Expr({1: [rem]})
                _expr += __exprs_ * coeff
        if not _expr.expr or _expr.expr == {}:
            _expr.expr = {0: [{'': 0}]}
        return (
            _expr.simp() if not args and not kwargs else _expr.cal(*args, **kwargs)) if repeat == 1 else _expr.lin_diff(
            var_, repeat - 1, *args, **kwargs)

    def __rsub__(self, other):
        return self - other

    def simp(self, psort=False, desolve=True):
        """
            Simplifying Expr Objects

            Call on the simp method when simplification like arrangements,
            collection of like terms, removing Zero terms

            y = - cba -xzqa + 3 - 2x + 4bac + 5 - 7zaqx - 7x - abc + 2qax + 8zxaq + 9x-3bca - 1

            >>> y = Expr('- cba -xzqa + 3 - 2x + 4bac + 5 - 7zaqx - 7x - abc + 2qax + 8zxaq + 9x-3bca - 1')
            >>> ysimp = y.simp()

            Which gives - abc + 7 + 2aqx

            Note that multiplication, division, exponents, differentiation, cal, and most operation call this before
            returning, so such method would returned a simplified Expr Object, so calling this method may not be neccesaary
            after such method.

            Simplify,
            - x^4î^2 - î^2x^2 - x^2î^2 - î^2 - x^5î - îx^3 - x^3î - îx + x^5î + x^3î + x^3î + xî + x^6 + x^4 + x^4 + x^2

            >>> E = Expr('- x^4.i^2 - .i^2x^2 - x^2.i^2 - .i^2 - x^5.i - .ix^3 - x^3.i - .ix + x^5.i + x^3.i + x^3.i + x.i + x^6 + x^4 + x^4 + x^2')
            >>> E.simp()
            which gives 3x^4 + 3x^2 +  1  + x^6
        """

        ff = format(self)
        alpha = set(self.variables)
        alpha = sorted(alpha.union({char for char in ('s', 'c', 't', 'l', 'a') if char in ff}))
        res = {}
        sim = {}
        arr = {}
        arr_ = {}
        _arr_ = []
        end = 0
        pbj = {}
        lbj = {}
        consts_ = []
        sk2 = 1
        # Arranging each term in order
        s = str({'': 0})
        for coeff, var in self.expr.items():
            if var == [{}]:
                var = [{'': 0}]
            if not alpha:
                alpha__ = range(len(var))
            sk1 = 1
            for var_ in var:
                usse = []
                for alpha_ in alpha if alpha else alpha__:
                    if len(usse) == len(var_):
                        break

                    if str(var_) == s:
                        consts_.append(coeff)
                        sk1 -= 1
                        sk2 = 0
                        break

                    sk1 = 11

                    for nq, var__ in enumerate(var_):
                        if nq in usse:
                            continue
                        if var__ and not var_[var__]:
                            end += 1
                            usse.append(nq)
                            continue

                        elif not isinstance(var__, str) and startwith(var__) == alpha_:
                            pbj[var__] = var_[var__]
                            usse.append(nq)

                        elif numable(var__):
                            lbj[var__] = var_[var__]
                            usse.append(nq)

                        elif isinstance(var__, str) and (not var__ or (alpha_ == var__ and var_[alpha_])):
                            if var__:
                                usse.append(nq)
                            if not var__ and len(var_) - 1:
                                continue
                            arr[var__] = var_[var__]

                for keys, values in join(pbj, lbj).items():
                    arr[keys] = values
                    pbj = {}
                    lbj = {}

                if end:
                    arr[''] = 0

                if not arr:
                    arr = {'': 0}
                if sk2 or (not sk2 and str(arr) != s):
                    _arr_.append(arr)
                arr = {}
            if sk1 > 0:
                arr_[coeff] = _arr_
            _arr_ = []
        sort = Expr({})
        used = []

        for coeff, var in arr_.items():
            if var == [{}]:
                arr_[coeff] = [{'': 0}]
        # Odering the terms of the Expressions
        alphaa = copy(alpha)
        for count in complex_id:
            if count in alphaa:
                alphaa.remove(count)
        alphaa = ['î', 'ĵ', 'ǩ'] + alphaa
        for alpha_ in alphaa:
            for count, expre in enumerate(Expr(arr_).struct):
                if alpha_ in format(expre) and not count in used:
                    # To support Imaginary number
                    try:
                        if alpha_ in complex_id:
                            cof, imj = expre.__extract__
                            pw = imj[alpha_]
                            powc = abs(pw) % 4
                            cof *= -1 if powc in (2, 3) else 1
                            if powc % 2:
                                imj[alpha_] = powc % 2
                            else:
                                imj.pop(alpha_)
                            if not imj: imj = {'': 0}
                            expre = Expr({cof: [imj]})
                            if pw < 0:
                                expre = -expre
                    except KeyError:
                        pass
                    sort += expre if desolve else {expre}
                    used.append(count)

        re_sort = Expr({})
        # To simplify Complex Numbers
        for exprs in sort.struct:
            count = 0
            for restrict in complex_id:
                if restrict in format(exprs):
                    count += 1
            if count < 2:
                re_sort += exprs if desolve else {exprs}
        sort = re_sort
        del re_sort
        for count, exprs in enumerate(Expr(arr_).struct):
            exprs_ = format(exprs)
            sett = 3
            for alphas in alpha:
                if alphas in exprs_:
                    sett = 0
                    break
            if sett and count not in used:
                inr = '^(0.5)' in exprs_

                s_exp = Expr(exprs, skip=not (desolve)) if not inr else Expr(exprs, skip=not (desolve)).inroots

                sort += s_exp if desolve else {s_exp}
        arr_ = sort.expr

        # Simplifying other Classes
        _arr = {}
        for coeff, var in arr_.items():
            _arr_list = []
            rcoeff = coeff
            for vars_ in var:
                _arr_list_dict = {}
                restructure = False
                fracs = Frac(Expr('1'), Expr('1'))
                while True:  # Unify Fraction Products

                    if restructure:
                        fracs *= Expr({coeff: [_arr_list_dict if _arr_list_dict else {'': 0}]})
                        den = numity(get_den(fracs))
                        if den and den == 1:
                            fracs = fracs.num

                        _arr_list_dict = {fracs: 1}
                        if 1 not in _arr:
                            _arr[1] = []
                        _arr[1].append(_arr_list_dict)

                        break
                    for _vars, pows in vars_.items():
                        generic = []
                        if len(vars_) > 1 and (getter(_vars, 'name') == 'Fraction' or (
                                getter(_vars, 'name') == 'Expr' and '/' in format(_vars))):
                            if getter(_vars, 'name') == 'Expr' and len(_vars) == 1:
                                ff, __var = _vars.__extract__
                                _vars = ff * list(__var)[0]
                            fracs *= _vars ** pows
                            restructure = True
                        elif not isinstance(_vars, str):
                            if getter(_vars, 'name') == 'Expr' and isinstance(pows, int):
                                if len(_vars) == 1:
                                    if numable(_vars):
                                        _arr_list_dict[_vars.simp()] = pows
                                        continue
                                    ff, __var = _vars.__extract__
                                    arr_l = {}
                                    for items, pows_ in __var.items():
                                        if getter(items, 'name'):
                                            items = items.simp()
                                        arr_l[items] = pows_ * pows
                                    generic.append(arr_l)
                                elif pows == 1:
                                    generic.append(_vars)
                                else:
                                    _arr_list_dict[_vars.simp()] = pows
                            else:
                                if getter(_vars, 'name') == 'trig':
                                    _arr_list_dict[_vars ** pows] = 1
                                else:
                                    _arr_list_dict[_vars.simp()] = pows

                        else:
                            _arr_list_dict[_vars] = pows
                    else:
                        if not restructure:
                            break
                if restructure:
                    continue
                for items in generic:
                    if not isinstance(items, dict):
                        for coef_, items in items.expr.items():
                            coef_ *= coeff
                            for letters, powd in _arr_list_dict.items():
                                for letter in items:
                                    if letters not in letter:
                                        letter[letters] = powd
                                    else:
                                        letter[letters] += powd
                                    if '' in letter:
                                        letter.pop('')
                                    if not isinstance(letter[letters], (int, float)):
                                        letter[letters] = powd.simp()

                            if coef_ not in _arr:
                                _arr[coef_] = items
                            else:
                                for items_ in items:
                                    _arr[coef_].append(items_)
                        _arr_list_dict = {}
                    else:
                        ff *= coeff
                        if ff in _arr:
                            _arr[ff].append(items)
                        else:
                            _arr[ff] = [items]
                if _arr_list_dict:
                    _arr_list.append(_arr_list_dict)

            if coeff not in _arr and _arr_list:
                _arr[coeff] = []
            for fracs in _arr_list:
                _arr[coeff].append(fracs)

        # Collecting like times
        for coeffs_ in consts_:  # Adding integers or floats
            if coeffs_ not in _arr:
                _arr[coeffs_] = []
            _arr[coeffs_].append({'': 0})
        for coeff, var in _arr.items():
            if not coeff:
                continue
            for var_ in var:
                _sorted = [{_var_: var_[_var_] for _var_ in sorted(var_)}]
                updates = Dict(_sorted)
                if not updates in res:
                    res.update({updates: coeff})
                else:
                    res[Dict(_sorted)] += coeff
        # Restoring the dict structure and removing every zero coefficient
        for coeff, var in res.items():
            if not var or not coeff:
                continue
            coeff_ = []
            for coeffs in coeff.dic:
                _coeffs = {}

                for coeffs_, counter in coeffs.items():
                    if counter:
                        _coeffs[coeffs_] = counter
                if _coeffs:
                    coeff_.append(_coeffs)
            if var and not coeff_:
                coeff_ = [{'': 0}]
            var = alnum(var)
            if var in sim:
                sim[var].append(coeff_[0])
            else:
                sim.update({var: coeff_})
        if not sim:
            sim = {0: [{'': 0}]}
        new_simp = self.new
        new_simp.expr = sim
        return new_simp if not psort else new_simp.__psort__(self, False)

    @property
    def const(self):
        const = [x for x in self.struct if not x.vars]
        return sum(const).simp() if const else Expr('')

    @property
    def transform(self):
        """
            Expr Objects Also support Transforms.
            calling this method will return the Transform class.

            This Transform class contains the laplace transform, z-transform, fourier transform
            hilbert transform.

            Laplace Transforms
            ==================

                To obtain the lapace transform use the laplace method of the Transform class
                this method takes in two arguments, the input variable and the output variable of the transform

                e.g Find the Lapalace Transform of 4e^(2t) + 3cosh(4t)

                >>> L = Expr('4.e^(2t) + 3cosh(4t)')
                >>> L.transform.laplace()

                This will give ((2s^2 - 2s - 16)/(s^3 - 2s^2 - 16s + 32))

                find the Laplace Transform of 2sin(3t) + 4sinh(3t)

                >>> L = Expr('2sin(3t) + 4sinh(3t)')
                >>> L.transform.laplace()

                This will give ((18s^2 + 54)/(s^4 - 81))

                The default parameter for input variable and out variable are t
                and s respectively.

                if X(t) = e^(3t)sinh(2t) find the laplace in terms of ω

                >>> Xt = Expr('.e^(3t)sinh(2t)')
                >>> Xt.transform.laplace(out_var = 'omega')

                which is (2/(ω^2 - 6ω + 5)

                Find the laplace transform of f(ω) = 3e^(-ω) + cos(2ω) - 3sin(2ω) in
                terms of φ

                >>> f = Expr('3.e^(-omega) + cos(2omega) - 3sin(2omega)')
                >>> f.transform.laplace('omega','phi')

                Laplace transforms can also be expressed in another Expr Object

                Find the laplace transform of 4 + 5e^(2t) in terms of s + γ

                >>> L = Expr('4+5.e^(2t)')
                >>> L.transform.laplace(out_var = 's + gamma')

                Which gives ((9s + 9γ - 8)/(s^2 + γ^2 + 2sγ - 2s - 2γ))

        """
        return Transforms(self)

    def integrate(self, var='x', repeat=1, *args, **kwargs):
        """
            The Integral of Expr Objects
        """
        _expr = Expr({})
        for expr_ in self.struct:
            coeff, _var = expr_.__extract__
            const, integrand, _mul_ = {}, {}, Expr({1: [{'': 0}]})
            print(expr_, 'sef')
            for var_, pow_ in _var.items():
                if var in replacer(
                        format(var_),
                        'sin', 'cos', 'tan',
                        'cosec', 'sec', 'log',
                        'ln', 'cot'
                        ) or (not isinstance(pow_, (int, float)) and var in replacer(
                                                                            format(pow_),
                                                                            'sin', 'cos', 'tan',
                                                                            'cosec', 'sec', 'log',
                                                                            'ln', 'cot'
                                                                            )
                ):
                    integrand[var_] = pow_
                else:
                    const[var_] = pow_
                    print('gg', integrand)
            if not len(integrand) - 1:
                _var = list(integrand)[0]
                pow_ = integrand[_var]
                print(type(_var), 'fbrfb')
                if isinstance(_var, str):
                    if _var == chr(553):
                        const[_var] = pow_
                        _mul_ /= pow_.lin_diff(var)
                    elif isinstance(pow_, (int, float)):
                        if pow_ == -1:
                            const[toClass(f'ln({_var})')] = 1
                        else:
                            const[_var] = pow_ + 1
                            coeff /= pow_ + 1
                elif getter(_var, 'name') == 'trig':
                    _expr += coeff * (_var ** pow_).integrate(var)
                    print(format((_var ** pow_).integrate(var)), _expr)
                elif getter(_var, 'name') == 'Expr':
                    print(_var, 'dvd')
                    if pow_ == -1:
                        const[toClass(f'ln({_var}')] = 1
                        _mul_ /= _var.lin_diff(var)
                        print(const, 'yyh', _mul_)
                    if len(_var) == 2 and pow_ == -.5:
                        cf = _var.coeff(f'{var}^2')
                        print(cf, 'mm')
                        if cf < 0:
                            for s_expr in _var.struct:
                                print(s_expr, 'gn')
                                if numable(s_expr):
                                    cf = num(abs(cf) ** .5)
                                    const[toClass(f'arcsin({cf / s_expr ** .5} * {var})')] = 1
                                    coeff /= cf
                    else:
                        const[Expr(_var)] = pow_ + 1
                        _mul_ /= (pow_ + 1) * _var.lin_diff(var)
                elif getter(_var, 'name') == 'Fraction':
                    _expr += coeff * (_var ** pow_).integrate(var)
                    print(format((_var ** pow_).integrate(var)), _expr)
            print(const, 'tycn')
            if not integrand:
                const[var] = 1
            if const:
                _mul_ *= Expr({coeff: [const]})
                print(_mul_, 'hghgh', {coeff: [const]}, 'bb f', Expr({coeff: [const]}))
                _expr += _mul_
                print('rrbaab ', Expr({coeff: [const]}).expr)
                v = Expr({coeff: [const]})
                print(str(v), 'ygn', format(v), 'thg', repr(v))
            elif not integrand:
                _mul_ *= Expr({coeff: [{var: 1}]})
                _expr += _mul_

        return (_expr.simp() if not args and not kwargs else _expr.cal(*args,
                                                                       **kwargs)) if repeat == 1 else _expr.integrate(
            var_, repeat - 1, *args, **kwargs)


    @property
    def figure(self):
        for exprs in self:
            if numable(exprs):
                return num(exprs)
        return False

    @classmethod
    def pow(cls, exprs, var=''):
        ex = 0
        exp = cls(exprs) if isinstance(exprs, str) else exprs
        for coeff, _var in exp.expr.items():
            for var_ in _var[0]:
                ex += _var[0][var_] if not var else 0 if var and var_ != var else _var[0][var_]
        return ex

    def powof(self, var, suppress=False):
        """returns the max index of a variable, raise an exception if not found except suppress is set to True"""

        power = self.get_powers(var)
        if not power and not suppress:
            raise QueryError(f'{var} is not present in {self}')
        return max(power) if isinstance(power, tuple) else power

    @property
    def cast(self):
        return Expr({1: [{self: 1}]})


    def ppowers(self, sep=False):
        var_list, self_ = self.vars, self.duplicate()
        working_vars, power, index, a , b, c, fig_used, chain_list = {}, None, {}, 1, 1, {}, False, []
        for var in var_list:
            powers_ = self.get_powers(var)
            power, powers = num_mul(*powers_)
            if power is None: continue
            if powers == 1:
                continue
            if powers not in index:
                index[powers] = num(max(powers_)/power)
            elif powers in index and index[powers] != num(max(powers_)/power):
                continue
            try:
                coeff, coeff_2 = break_pq(self.coeff(f'{var}^{max(powers_)}'), index[powers])
            except ImportError:
                if len(working_vars) < len(index):
                    index.pop(powers)
                continue
            if not powers in c: c[powers] = abs(coeff)
            elif c[powers] != abs(coeff): continue
            const = -1 if (powers in working_vars and self.coeff(f'{var}^{max(powers_) - power}')._coeff < 0) or coeff < 0 else 1
            if powers in working_vars:
                working_vars[powers][var] = (power, num(const * coeff_2 ** (1/index[powers])))
            else:
                working_vars[powers] = {var: (power, num(const * coeff_2 ** (1/index[powers])))}
        for i, working_var in working_vars.items():
            if not fig_used and len(working_var) != 2:
                fig = self.figure
                if list(working_var)[0][0] not in (-1, 1) and intable(abs(fig) ** (1/index[i])):
                    working_var[num(abs(fig) ** (1/index[i]))], fig_used = (1, fig/abs(fig),), True
                    conj = True
            if len(working_var) == 2:
                x, y = list(working_var)
                p, a = working_var[x]
                q, b = working_var[y]
                s, a, p = '+' if b > 0 else '', '' if a == 1 else '-' if a == -1 else a, '' if p == 1 else f'^{p}'
                b, q = '' if b == 1 else '-' if b == -1 else b, '' if q == 1 else f'^{q}'
                expected = Expr(f'({a}{x}{p} {s} {b}{y}{q})^{index[i]}')
                try:
                    self_ = self_.replace(expected, strict=True)
                    chain_list.append(Expr({c[i]: [{Expr(f'({a}{x}{p} {s} {b}{y}{q})'): index[i]}]}))
                except QueryError:
                    if conj:
                        s = '+' if s == '-' else '-'
                        expected = Expr(f'({a}{x}{p} {s} {b}{y}{q})^{index[i]}')
                        try:
                            self_ = self_.replace(expected, strict=True)
                            chain_list.append(Expr({c[i]: [{Expr(f'({a}{x}{p} {s} {b}{y}{q})'): index[i]}]}))
                        except QueryError:
                            pass

        return (sum(chain_list) + self_) if not sep else (sum(chain_list), self_)


    @property
    def new(self):
        """
            Expr Objects has two main properties.
            The Expression itself and its internal property (attributes)
            If Expr is an Expr Object, Use:
                1. deepcopy to copy all properties and attributes; deepcopy(Expr)
                2. copy to shallow copy the Expression only.
                   Note that there may be discrepancies in shallow copies of nested Expr Objects. e.g hypolic like cosh objects
                   and this is because they are trig object with special attribute that identify them as
                   hyperbolic, which may not be copied; copy(Expr)
                3. duplicate to deepcopy only the Expression; Expr.duplicate()
                4. new to return an empty expression with a copy of all the attributes.
                   Note that all the attributes of the Expressions will be ignored; new(Expr)



        """
        return deepcopy(self, 'expr')

    def factorize(self, perfect=True):
        list_expr = list(self.struct)
        common = Expr(GCD(*list_expr))
        if len(self) == 1: return self
        rem_expr_ = factor_out(self, common)
        adder, rem_expr = difference_powers(rem_expr_, sep=True)
        adder_2 = rem_expr.ppowers(sep=True) if not isinstance(rem_expr, (int,float)) else (0, rem_expr)
        adder += adder_2[0]; rem_expr = adder_2[1]
        if not rem_expr: return adder
        elif adder: return adder + rem_expr.factorize()
        trial_1, inpart = group_factor(rem_expr, proofing=True), False
        if trial_1:
            if GCD(*list(trial_1.struct)) != 1:
                new_factor = trial_1.factorize()
            else:
                new_factor, inpart = trial_1, True
        else:
            new_factor = rem_expr
        new_factor = adder + new_factor if adder else new_factor
        if numable(common):
            factorized = new_factor * common
        else:
            coeff = common._coeff
            if inpart or not trial_1:
                if common != 1: new_factor = new_factor.cast
            common /= coeff
            factorized = common.cast if common != 1 else common
            factorized.expr[1][0].update(new_factor.__extract__[1])
            if '' in factorized.expr[1][0]:
                factorized.expr[1][0].pop('')
            factorized *= coeff
        return factorized

    @classmethod
    def pow_index(cls, exprs):
        ex = []
        exp = cls(exprs) if isinstance(exprs, str) else exprs
        for coeff, _var in exp.expr.items():
            for var_ in _var[0]:
                ex.append(_var[0][var_])
        return max(ex)

    def pow_order(self):
        return 1 if not self.vars else max([self.pow_index(exprs) for exprs in self.struct if not numable(exprs)])

    def npow_order(self):
        return 1 if not self.vars else min([self.pow_index(exprs) for exprs in self.struct if not numable(exprs)])

    @property
    def islinear(self):
        """
            returns True if the Expression is linear else False
        """

        return True if self.pow_order() == self.npow_order() == 1 else False

    def get_power(self, var):
        """return the power of a variable in an ExprObj

            returns tuple of the powers if the variable is raised to different powers
            returns a term if the variable is raised once, returns None if the variable is absent
        """
        pow_list = []
        for exprs in self.struct:
            for var_, pows in exprs.expr[exprs._coeff][0].items():
                if str(var_).replace(' ', '') == str(var).replace(' ', ''):
                    if not pows in pow_list:
                        pow_list.append(pows)
                    break

        return pow_list[0] if len(pow_list) == 1 else tuple(pow_list) if pow_list else None

    def get_powers(self, var):
        """return the power of a variable in an ExprObj

            returns tuple of all the powers if the variable is raised to different powers
            returns a term if the variable is raised once, returns None if the variable is absent
        """
        pow_list = []
        for exprs in self.struct:
            for var_, pows in exprs.expr[exprs._coeff][0].items():
                if str(var_).replace(' ', '') == str(var).replace(' ', ''):
                    pow_list.append(pows)
                    break
        return tuple(pow_list) if pow_list else []

    def unify(self, strict=False):
        """
            If the Expr Objects contains Fractions, this method combine all terms
            into a single term.

            if strict is True, terms with negative powers will be treated as Fractions as well
        """
        out = Expr({})
        frac_ = Frac(Expr('0'), Expr('1'))
        for exprs in self.struct:
            if '/' in format(exprs) or (strict and '^-' in format(exprs)):
                coeff, var = exprs.__extract__
                if len(var) > 1:
                    expr = Expr('1')
                    for var_, pow_ in var.items():
                        if getter(var_, 'name') == 'Fraction' or (strict and isinstance(var_,
                                                                                        str) and isinstance(pow_,
                                                                                                            (int,
                                                                                                             float)) and pow_ < 0):
                            if isinstance(var_, str):
                                frac = Frac(Expr('1'), Expr(var_) ** abs(pow_))
                            else:
                                frac *= var_ ** pow_
                        else:
                            if getter(var_, 'name') is None:
                                var_ = Expr(var_) ** pow_
                            expr *= var_
                    frac *= expr
                else:
                    var_ = list(exprs.expr[coeff][0])[0]
                    pow_ = exprs.expr[coeff][0][var_]
                    if isinstance(var_, str) and isinstance(pow_, (int, float)) and pow_ < 0:
                        frac = Frac(Expr('1'), Expr(var_) ** abs(pow_))
                    else:
                        if getter(var_, 'name') == 'Expr':
                            cf, var_ = var_.__extract__
                            var__ = list(var_)[0]
                            pow_ *= var_[var__]
                            frac = cf * var__ ** pow_
                        else:
                            frac = var_ ** pow_
                frac_ += frac * Expr(coeff)
            else:
                out += exprs
        return self.new + (frac_ + out).simp()

    def subject(self, var, eq=0):

        """Making var subject of Formula of the expression when == eq

            if y^2 = 3x^3 + 4; make x the subject

            >>> y = Expr('3x^3 + 4')
            >>> y.subject('x', 'y^2')
            (0.3333333333333333y^2 - 1.3333333333333333)^0.3333333333333333
        """

        concat = (self - eq).reform()

        index = concat.get_power(var)

        if isinstance(index, tuple):
            raise OperationNotAllowed('You cant find the subject of higer degree')
        if index is None:
            raise InvalidOperation(f'{var} is not present in {self}, hence subject aborted')
        ord_cat, var_cat = concat.split(var)
        div = []
        for _vars in var_cat.struct:
            if _vars.coeff(f'{var}^{index}' if index != 1 else f'{var}'):
                div.append(_vars.coeff(f'{var}^{index}' if index != 1 else f'{var}'))
            else:
                ord_cat += _vars
        return (-ord_cat / sum(div)) ** (1 / index)

    def visualize(self, color='g', linewidth=2, *args, **kwarg):
        """
            This method returns the Visual Class for visualizing Graphs

            if f(x) = 3xcos(x) - 2sinh(2x) + 3
            To Visualize this Function on the graph with in range -5 to 7

            >>> Fx = Expr('3tcos(t) - 2sinh(2t) + 3')
            >>> Fx.visualize(t = Range(-5, 7)).plot

            if visualize the sinusoid cos(ωn + φ) given that ω = 'pi/6', φ = 'pi/4', within n = 0 and n = 36
            >>> X = Expr('cos(omegan + phi)')
            >>> X.visualize(omega = 'pi/6', phi = 'pi/4', n= Range(0,36)).plot

        """
        var_list = list(self.vars)
        var_list += [rev(greek_map)[greeks] for greeks in var_list if greeks in rev(greek_map)]
        var = {}
        kwargs = {}
        values = {}

        for keys, _values in kwarg.items():
            if keys in var_list:
                if isinstance(_values, Range):
                    _values.step = .05
                    var.update({keys: list(_values)})
                else:
                    values.update({greek_map[keys] if keys in greek_map else keys: _values})



            else:
                kwargs.update({keys: values})

        return Visualize(var, self.cal(values) if values else self, color, linewidth, *args, **kwargs)

    @property
    def variables(self):
        """
            This property gives the all variables in an Expr Objects including constant
        """
        var_list = set()
        for exprs in self.struct:
            for keys, values in exprs.expr.items():
                for value in values[0]:
                    if isinstance(value, str):
                        if value.isnumeric():
                            continue
                        var_list.add(value)
                    elif getter(value, 'name'):
                        var_list = var_list.union(set(value.variables))
                    if not isinstance(values[0][value], (int, float)):
                        var_list = var_list.union(set(values[0][value].variables))
        var_list = sorted(var_list)
        if '' in var_list:
            del var_list[var_list.index('')]

        return var_list

    @property
    def vars(self):
        """
            This property gives the all variables in an Expr Objects excluding constant
        """
        variables = self.variables
        for vars_ in copy(variables):
            if vars_ in constants or vars_ in complex_id:
                variables.remove(vars_)
        return tuple(variables)

    @property
    def constants(self):
        """
            This property gives the all constants in an Expr Objects only
        """
        constant = []
        for vars_ in self.variables:
            if vars_ in constants:
                constant.append(vars_)
        return constant

    @property
    def deg(self):
        """
            This property returns the degree of an Expression
        """
        pows = []
        for exprs in self.struct:
            pows.append(self.pow(exprs))
        return max(pows) if pows else 0

    def __delitem__(self, other):
        """
            Expr Object support term deletion

            >>> Fx = Expr('3x - 2alpha + omegat - cos(alpha - omegat)')
            Now Fx = 3x - 2α + ωt - cos(α - ωt)
             To delete the 2nd term
            >>> del Fx[2]
            To delete the last term
            >>> del Fx[-1]
        """
        new = self.new
        if other == 0:
            raise UnacceptableToken('Index starts from 1')
        if other > len(self):
            raise IndexError(f"Can't reach {th(other)} as the expression has a length of {len(self)}")
        if other < 0:
            del self[len(self) + other + 1]
            return
        for count, exprs in enumerate(self.struct):
            if not count - other + 1:
                continue
            new += exprs
        self.expr = new.expr

    def __setitem__(self, other, value):
        """
            Expr Object support term deletion

            >>> Fx = Expr('3x - 2alpha + omegat - cos(alpha - omegat)')
            Now Fx = 3x - 2α + ωt - cos(α - ωt)
             To change the 2nd term to -sinh(2α )
            >>> Fx[2] = '-sinh(2α)'
            To delete the last term
            >>> del Fx[-1]
        """
        if other == 0:
            raise UnacceptableToken('Index starts from 1')
        if other > len(self):
            raise IndexError(f"Can't reach {th(other)} as the expression has a length of {len(self)}")
        if other < 0:
            self[len(self) + other + 1] = value
            return
        new = self.new
        for count, exprs in enumerate(self.struct):
            new += value if not count - other + 1 else exprs
        self.expr = new.simp().expr

    @property
    def islin(self):
        """
            This Method returns True if the Expression is of degree 1
        """
        return True if self.deg == 1 else False

    def pop(self, other):
        """
            This method remove a term from the Expression and return it
            if the argument is an integer let say n, it will remove and
            return the nth term of the expression else it will wipe and
            return the item
            >>> Fx = Expr('3x - 2alpha + omegat - cos(alpha - omegat)')
            >>> x = Fx.pop('omegat')
            x is now ωt and has been removed from Fx
        """
        if isinstance(other, int):

            sv = self[other]
            del self[other]
        else:
            sv = Expr(other)
            self.wipe(other)

        return sv

    @property
    def __extract__(self):
        coeff = self._coeff
        var = self.expr[coeff][0]
        return coeff, var

    @property
    def isnum(self):
        """
            This method return True if the Expression is an integer or float
        """
        return self.variables == []

    @property
    def numable(self):
        """
            This method return True if the Expression can be converted to a number
        """
        return bool(self.vars)

    def remove(self, other):
        """
            To remove an item from an Expression
            >>> Fx = Expr('3x - 2alpha + omegat - cos(alpha - omegat)')
            >>> Fx.remove('-2alpha')
            Note that if the item is not present no exception is raised
            Also note that you can remove more than one item
            >>> y = Expr('x + y -pcos(-3p) - log(6x) + ln(2x+1)')
            >>> y.remove('x - log(6x) + y')
        """
        if not getter(other, 'name') == 'Expr':
            other = Expr(f'{other}')
        for exprs in other:
            try:
                del self[self.index(exprs)]
            except QueryError:
                pass

    def clear_frac(self, proofing=False):
        """Equating the expression to Zero and clear fractions and negative indices

           use the proofing argument to suppress any unknown error encountered,
           instead the Expr Object itself is returned
        """
        form = self.duplicate()
        form_ = format(form)
        counts = 0
        while True:
            den = get_den(form)
            counts = len(den) if not counts else counts
            if not den:
                break
            form *= den[0]
            counts -= 1

            if not counts and format(form).count('/') > form_.count('/'):
                if proofing:
                    raise ImprobableError
                else:
                    return self

        return form

    def replace(self, term_1, term_2 = '', strict=False):
        if strict and term_1 not in self:
            raise QueryError(f'{term_1} is not in {self}')
        return (self - term_1 + term_2).simp()

    def reform(self):
        """ return an equivalent Expr

            The reform method restructure the Expr by assuming it equals zero

            Rewrite y + 1/x - 4

            >>> Expr('y + 1/x - 4').reform()
            xy + 1 - 4x

            Rewrite 1 /(sqrt(x^2 - 24) + x) + 3/( - sqrt(x^2 - 24) + x) = 11/12
            >>> Expr('1 /(x + sqrt(x^2 - 24)) + 3/(x - sqrt(x^2 - 24)) - 11/12').reform()
            176x - 12x^2 - 580

            Rewrite the resulting function when a function mapping given by
                f(x,y) = 2x^2 + 2xy + 3x + 3y^2 - 2y - 2, was mapped into y - plane
                by a function given by f(y) = (-26-5y^2-4y)/(16y -5)

            >>> fxy = Expr('2x^2 + 2xy + 3x + 3y^2 - 2y - 2')
            >>> fy = Expr('(-26-5y^2-4y)/(16y -5)')
            >>> result = fxy.cal(x = fy)
            Now the resulting function, result is now
                329y^2/128 + 4(8.668212890625y/(16y - 5)) + 2(769.4122467041016/(256y^2 - 160y + 25))
                - 3275y/1024 + 103( - 27.73828125/(16y - 5))/64 + ( - 55.4765625y/(16y - 5))
                - 91791/32768
            To rewrite this function in cool form
            >>> result.reform()
            which gives 658y^4 - 1230y^3 - 474y^2 - 242y + 1692

            This can be done in a single line
            >>> Expr('2x^2 + 2xy + 3x + 3y^2 - 2y - 2').cal(x = '(-26-5y^2-4y)/(16y -5)').reform()
            which also yield 658y^4 - 1230y^3 - 474y^2 - 242y + 1692
        """
        r = len(self)
        form_ = self.desolved
        form = format(form_)
        rd = form.count('/')
        if '/' in form or '^-' in form:
            form_ = form_.clear_frac()
        s, y = Expr({}), Expr({})
        f_list = []
        add = 0
        while True:

            for exprs in form_.struct:
                coeff, var = exprs.__extract__
                for var_, pow_ in var.items():
                    if not isinstance(var, (str, int, float)) and isinstance(pow_, float):
                        f_list.append(Fraction(pow_).limit_denominator().denominator)
                        if add >= 2:
                            y += exprs
                        else:
                            s += exprs
                        add += 1
                        break
                else:
                    y += exprs
                if len(y) + len(s) == len(form_) and s:
                    break
            else:
                return form_
            fac = Num(*f_list).LCM()
            form_ = sum([-(-y) ** fac, s ** fac]).rindex().desolved
            f_list, s, y = [], Expr({}), Expr({})
            add = 0

    def rindex(self):
        """Factorise terms with the same index"""
        tind = Expr({})
        for exprs in self.struct:
            coeff, var = exprs.__extract__
            p_s = {}
            _var_ = {}
            for var_, pow_ in var.items():
                if pow_ not in p_s:
                    p_s[pow_] = []
                p_s[pow_].append(var_)

            for ind, lis in p_s.items():
                _var_[Mul(lis) if len(lis) > 1 else lis[0]] = ind
            tind += Expr({coeff: [_var_]})
        return tind

    def wipe(self, other):
        """
            The wipe an expression from a Expr Objects, the items
            are verified to be present before removal

            This works like the remove method: however, an exception
            (InvalidOperation)
            is raised if one of the items to be removed is not present
        """
        if not getter(other, 'name') == 'Expr':
            other = Expr(f'{other}')
        state = True
        for exprs in other:
            if exprs not in self:
                state = False
                mis = exprs
                break
        if not state:
            raise InvalidOperation(f"Can't continue as {mis} is not in the expression")
        self.remove(other)

    def __psort__(self, init='', direct=True):

        if not self:
            return self
        self_ = self.simp(True) if direct else self
        vars_ = self.new
        pows = []
        __vars__ = {}
        var_pt = []
        # Gathering powers
        for count, exprs in enumerate(self_):
            pows.append(self.pow(exprs))
            if not self.pow(exprs):
                var_pt.append(count + 1)
        pows_ = list(set(pows))
        pows_.sort()
        pows_.reverse()
        used = []

        # Reodering
        for memebers in pows_:
            for alphas in alpha:
                for count, items in enumerate(pows):
                    if items != memebers or count in used:
                        continue
                    if alphas in str(self_[count + 1]):
                        vars_ += self_[count + 1]
                        used.append(count)
        for var_pts in var_pt:
            sett = 6
            for alphas in alpha:
                if alphas in str(self_[var_pts]):
                    sett = 0
            if sett:
                vars_ += self_[var_pts]
        for coeff, var in vars_.expr.items():
            if coeff:
                __vars__[coeff] = var
        return init if Expr(__vars__).replace(' ', '') == str(init).replace(' ', '') else Expr(__vars__).simp(True)

    def comp_equiv(self, other):
        for comp in complex_id:
            if self.coeff(comp) != other.coeff(comp):
                return False
        return True

    def equiv(self, other, limit='', monitor=False, scaling=False):

        if not limit:
            limit = {}
        if not getter(other, 'name') == 'Expr':
            other = Expr(f'{other}')
        all_vars = self.vars + other.vars
        scaler = ''
        for i in range(10):
            test_range = 25
            start = -25
            val_range = dict(zip(all_vars, [
                (random.randint(-10, 10) if i in str(self.pow(self)) else random.randint(-test_range, test_range)) for i
                in all_vars]))
            for var, rang in limit.items():
                val_range[var] = random.randint(rang[0], rang[1])
            try:
                v = alnum(self.cal(val_range, desolve=1))
                q = alnum(other.cal(val_range, desolved=1))
            except InvalidOperation:
                start = 1
                val_range = dict(zip(all_vars, [random.randint(start, test_range) for i in all_vars]))
                v = alnum(self.cal(val_range, desolve=1))
                q = alnum(other.cal(val_range, desolved=1))
            except ZeroDivisionError:
                start *= 2
                val_range = dict(zip(all_vars, [random.randint(start, test_range) for i in all_vars]))
                v = alnum(self.cal(val_range, desolved=1))
                q = alnum(other.cal(val_range, desolved=1))
            if not isinstance(v, (int, float)) or not isinstance(q, (int, float)):
                if self.iscomplex or other.iscomplex:
                    if self.real | other.real and self.comp_equiv(other):
                        continue
                raise ImprobableError('An Unknown Error occurred')
            while True:
                try:
                    if scaling:
                        scale = v / q
                        if isinstance(scaler, str):
                            scaler = scale
                            break
                        else:
                            if scaler == scale:
                                break
                    if v - q > 0.000001 or v - q < - .000001:
                        stop = 0
                        if monitor:
                            if stop == 3:
                                return False
                            limit = eval(input('Test fails, pls enter an update: '))
                            stop += 1
                            break
                        return False
                except (OverflowError):
                    test_range //= 2
                    start = -test_range
                    val_range = dict(zip(all_vars, [random.randint(start, test_range) for i in all_vars]))
                except InvalidOperation:
                    start = 1
                    val_range = dict(zip(all_vars, [random.randint(1, test_range) for i in all_vars]))
                except InvalidOperation:
                    start *= 2
                    test_range += start
                    val_range = dict(zip(all_vars, [random.randint(start, test_range) for i in all_vars]))

                else:
                    break
        return True

    def __or__(self, other):
        """
            To establish the equivalency of two Expr Objects

            if A = sin(7θ), B = 7sin(θ) - 56sin3(θ) + 112sin5(θ) - 64sin7(θ)

            To show that A is equivalent to B

            >>> A = Expr('sin(7theta)')
            >>> B = Expr('7sin(theta)-56sin3(theta)+112sin5(theta) - 64sin7(theta)')
            >>> A | B
            This should return True

            If  both Expression are not equivalent it will return False

            Note that the == may return False because for == to return True both the
            must be identical both in terms and have the same number terms

        """
        return self.equiv(other)

    def __getitem__(self, other):
        """
            To return a term at a given index.

            Note that Expr Objects indices start from 1

            >>> W = Expr('x^3 - 3x^2 - 7xy + 3')
            W[1] will give the first term which x^3
            W[3] will give the 3rd term, which is -7xy
            Negative indices counts from the back
            W[-1] will return the last term 3
            W[-3] will return third to the last
        """
        if other == 0:
            raise UnacceptableToken('Index starts from  1')
        if other > len(self):
            raise IndexError(f"Can't reach {th(other)} as the expression has a length of {len(self)}")
        if other < 0:
            return self[len(self) + other + 1]
        for count, expr_ in enumerate(self.struct, 1):
            if count == other:
                return expr_

    def __contains__(self, other):
        """
            Use the "in" to check if an expression is in the Expr Object

            W = Expr('2 + 3w - 3w^-2 + 3w^-4')
            '3w + 2' in W will return True
            '-2 + 3w' in W will return False

            For True to be returned, the coefficient and powers must match else False
            if coefficient doesn't matter in the matching use wrap method

        """
        if isinstance(other, (int, float)):
            other = str(other)
        truth_list = []
        other = Expr(other)
        self_list, done = list(self), []
        for exprs in other.struct:
            coeff, var = exprs.__extract__
            if (coeff, str(var),) in done:
                continue
            if coeff in self.expr:
                for dicts in self.expr[coeff]:
                    if not dict_uncommon(var, dicts):
                        done.append((coeff, str(var),))
                        break
                else:
                    return False
            else:
                return False
        return True

    def __abs__(self):
        """Return absolute value of a number"""
        al = alnum(self)
        if isinstance(al, (int, float)):
            return Expr(abs(al))
        try:
            return (self ** 2).solns()

        except Exception:
            raise Fizzle(f'Absolute Value of this expr {self} can not be determined')

    def __repr__(self):
        disp = ''
        for coeff in self.expr:
            disp_ = ''
            if not coeff:
                continue
            frac = Fraction(coeff).limit_denominator()
            if coeff < 0:
                numm_ = frac.numerator
                disp_ = f' - {abs(numm_)}' if numm_ != -1 else ' - 1' if self.expr[coeff][0] == {'': 0} else ' - '
            else:
                if disp:
                    disp_ += ' + '

                numm_ = frac.numerator
                disp_ += f'{numm_}' if numm_ != 1 else ' 1 ' if numm_ == 1 and self.expr[coeff][0] == {'': 0} else ''
            _var__ = ''
            frac_ = frac
            for count, expr_ in enumerate(self.expr[coeff]):
                _disp, _var__, emb = '', '', 0
                frac = frac_
                if count:
                    disp_ = ' - 1 ' if numm_ == -1 and (self.expr[coeff] == [{'': 0}] or self.expr[coeff][count] == {
                        '': 0}) else ' + 1' if numm_ == 1 and (
                            self.expr[coeff] == [{'': 0}] or self.expr[coeff][count] == {
                        '': 0}) else f' - ' if numm_ == -1 else f' - {abs(numm_)}' if numm_ < 0 else f' + {numm_}' if numm_ > 0 and numm_ != 1 else ' + ' if disp else ''
                for count_, var in enumerate(expr_):

                    _vva = format(var)
                    brac = False
                    powe = expr_[var]
                    if getter(var, 'name') == 'trig':
                        vva_ = repr(var)
                    else:
                        vva_ = format(var)
                    if getter(var, 'name') == "Expr" and len(var) == 1:
                        c, v = var.__extract__
                        for i in v:
                            if numable(i) or len(v) > 1 or (c != 1 and not isinstance(powe, (int, float))):
                                brac = True
                                break
                    _var__ = f'({vva_})' if ((brac or len(var) > 1) and len(_vva) > 1) or '/' in _vva and \
                                            get_exprs(_vva)[0] != _vva else vva_ if not coeff - 1 and not isinstance(
                        var, str) else f'({vva_})' if not isinstance(var, str) and expr_[var] != 1 else vva_
                    if not isinstance(var, str) and len(var) == 1:
                        if getter(var, 'name') == 'Expr':
                            if var._coeff - 1 and not numable(var) and isinstance(powe, (int, float)):
                                c, va = var.__extract__
                                frac *= c ** powe
                                emb = 1
                                _var__ = Expr({1: [va]})
                                _vva = format(_var__)
                                if getter(var, 'name') == 'trig':
                                    vva_ = repr(_var__)
                                else:
                                    vva_ = _vva
                                frac = Fraction(frac).limit_denominator()
                                coeff_ = frac.numerator
                                _var__ = f'({vva_})' if ((brac or len(var) > 1) and len(var) > 1) or '/' in _vva and \
                                                        get_exprs(_vva)[
                                                            0] != _vva else vva_ if not coeff_ - 1 and not isinstance(
                                    var, str) else f'({vva_})' if not isinstance(var, str) and expr_[var] != 1 else vva_

                                _coeff_ = ' - ' if coeff_ == -1 else f' - {abs(coeff_)}' if coeff_ < 0 else ' + ' if coeff_ == 1 else f' + {coeff_}' if disp else f'{coeff_}'

                        else:
                            if var.coeff - 1:
                                coeff_ *= var.coeff
                                emb = 1

                                _coeff_ = ' - ' if coeff_ == -1 else f' - {abs(coeff_)}' if coeff_ < 0 else '' if coeff_ == 1 else f'{coeff_}'

                                _var__ = _var__[start_alpha_index(_var__):]

                    if var and expr_[var] != 1:
                        pow_ = f"{expr_[var]}"
                        if pow_.endswith('.5'):
                            pow_ = int(alnum(pow_) * 2)
                            pow_ = '' if pow_ == 1 else '^' + str(pow_) if len(str(pow_)) == 1 or numable(
                                pow_) else f'^({pow_})'
                            _var__ = format(_var__)
                            if _var__[0] == '(' and _var__[-1] == ')':
                                _var__ = _var__[1:-1]
                            _var__ = f'sqrt({_var__})' + pow_
                        else:
                            pow_ = '^' + pow_ if len(pow_) == 1 or numable(pow_) else f'^({pow_})'
                            _var__ += pow_

                    _disp += _var__
                disp += (_coeff_ if emb else disp_) + _disp
                disp += f'/{frac.denominator}' if frac.denominator != 1 else ''

        if not disp:
            return '0'
        return disp

    def like(self, other):
        """
            The like method returns a list containing all the variables in two
            Expr Objects
        """
        if not getter(other, 'name') == 'Expr':
            other = Expr(other)
        var1 = self.variables
        var2 = other.variables
        return [var for var in var1 if var in var2]

    def tables(self, values='', fig=False, var=None, **value):
        """
            This method return table of values in Dict

            For function f(z) = 3z^3 - z^2 + 17z - 15
            Obtain a table for f(z) for the values
            (-10, -7, -5, -3/2, -1/7, 0 , 2, 31/7, -1)
            >>> fz = Expr('3z^3 - z^2 + 17z - 15')
            fz.tables((-10, -7, -5, -3/2, -1/7, 0 , 2, 31/7, -1))

            which will result to
            {-10:  - 3285, -7:  - 1212, -5:  - 500, -1.5:  - 423/8,
            -0.14285714285714285:  - 5988/343, 0:  - 15, 2: 39,
            4.428571428571429: 103324/343, -1:  - 36}

            For function f(t) = 3sin(t) - 3cos(3t) + 3
            Obtain a table for f(t) in range -2π to 2π,
            in the interval 1

            >>> ft = Expr('3sin(t) - 3cos(3t) + 3')
            >>> ft.tables(t = Range('-2pi', '2pi'))

            or
            >>> ft.tables({'t': Range('-2pi', '2pi')})

            {-6.283185307179586: 0ȩπ, -5.283185307179586: 7808341/919235,
            -4.283185307179586: 2227273/782218, -3.2831853071795862: 3822154/620807,
            -2.2831853071795862:  - 1789743/993215, -1.2831853071795862: 365338/152079,
            -0.28318530717958623: 61354/339341, 0.7168146928204138: 78sqrt(86)/367 + 197sqrt(54)/881 + 3,
            1.7168146928204138: 2646992/563725, 2.7168146928204138: 4232327/827795,
            3.7168146928204138: 854875/944423, 4.716814692820414: 1238/31059,
            5.716814692820414: 1506691/849236}



            if the Expression only has a unknown variable, only the
            value can be written
            since ft only has an unkown variable t
            >>> ft.tables(Range('-2pi', '2pi'))

            Note if more than one unkown is present, the value will be assign to the
            first variable return by the vars property

            for other intervals other than 1, add the interval to the arguments
            >>> ft.tables(Range('-2pi', '2pi', 1.5))

            which is
            {-6.283185307179586: 0ȩπ, -4.783185307179586: 4249478/641443,
            -3.2831853071795862: 3822154/620807, -1.7831853071795862:  - 639135/372163,
            -0.28318530717958623: 61354/339341, 1.2168146928204138: 5515417/653957,
            2.7168146928204138: 4232327/827795, 4.216814692820414:  - 1735887/660412,
            5.716814692820414: 1506691/849236}

            Setting the fig parameter to be True will return the values in Figures.



        """
        if not values and value:
            values = value
        if isinstance(values, dict):
            var = list(values)[0]
            values = values[var]
        if var is None:
            var = self.vars[0]

        return {value: (alnum(self._cal({var: value},
                                        desolved=True)) if fig else self._cal({var: value},
                                                                              desolved=True)) for value in values}

    def _tables(self, values, fig=False, var=None, **value):

        """
            This return the tables method in list
        """
        return Dict(self.tables(values, fig, var, **value)).list

    def __truediv__(self, other, split=False):
        """
            Division btwn Expr Objects.
            if f(x) =  - x^2î - î + x^3 + x and g(x) =  1  + x^2
            Simplify f(x)/g(x)

            >>> fx, gx = Expr('- x^2.i - .i + x^3 + x'), Expr('1 + x^2')
            >>> fx/gx
            will return - î + x

        """
        if not other:
            raise ZeroDivisionError('Division by Zero')
        numm = numity(other)
        if numm == 1:
            return self
        self_ = self.simp()
        val = {}
        val_ = {}
        if isinstance(other, (str, int, float)):
            other = Expr(other)
        if other.iscomplex and not other.isnum:
            return (self * other.conjugate) / (other * other.conjugate)
        if numable(other):
            return Expr({num(coeff / num(other)): alg for coeff, alg in self.expr.items()})
        if len(other) == 1:
            if '/' in format(other):
                coeff, var = other.__extract__
                _num = {}
                den = {}
                fracs = {}
                for var_, pows in var.items():
                    if isinstance(var_, str) or getter(var_, 'name') in ('trig', 'log'):
                        if pows < 0 or format(pows)[0].replace(' ', '') == '-':
                            _num[var_] = -1 * pows
                        elif pows > 0 or format(pows)[0].replace(' ', '') != '-':
                            den[var_] = pows

                    elif getter(var_, 'name') in ('Expr', 'Fraction'):
                        if pows < 0 or format(pows)[0].replace(' ', '') == '-':
                            fracs[var_] = -1 * pows
                        elif pows > 0 or format(pows)[0].replace(' ', '') != '-':
                            fracs[~var_] = pows

                    else:
                        raise ImprobableError('Unexpected Obj')
                _num = Expr({1: [_num]}) if _num else Expr(1)
                _mul = numity(self)
                if _mul:
                    _num *= _mul
                    _mul = 1
                else:
                    _mul = self

                if not den:
                    den = 1 / coeff * _num
                else:
                    den = Expr({1: [{Frac(_num, Expr({coeff: [den]})): 1}]})

                return (_mul * den * Expr({1: [fracs]})) if fracs else (_mul * den)

            val = self.new
            for exprs in self_.struct:
                for _coeff, _var in exprs.expr.items():
                    for coeff, var in other.expr.items():
                        for var_ in var[0]:
                            try:
                                if getter(var_, 'name') == 'trig':
                                    for vars_ in _var[0]:
                                        if getter(vars_, 'name') == 'trig' and vars_.unit == var_.unit:
                                            _pow = vars_.pow - var_.pow
                                            if _pow:
                                                exprs.expr[_coeff][0][var_.unit ** _pow] = 1
                                            exprs.expr[_coeff][0].pop(vars_)
                                            break
                                    else:
                                        raise KeyError
                                elif not exprs.expr[_coeff][0][var_] - var[0][var_]:
                                    exprs.expr[_coeff][0].pop(var_)
                                else:

                                    exprs.expr[_coeff][0][var_] -= var[0][var_]
                            except KeyError:
                                if getter(var_, 'name') == 'trig':
                                    exprs.expr[_coeff][0][var_ ** - var[0][var_]] = 1
                                else:
                                    exprs.expr[_coeff][0][var_] = - var[0][var_]
                    val += Expr({num(_coeff / coeff): [exprs.expr[_coeff][0]]})

        if len(other) > 1:
            try:
                if self | other:
                    return Expr('1')
            except Exception:
                pass
            if not self_.isdivisible(other):
                val = self.new
                if len(self_) > 1:
                    return sum([exprs / other for exprs in self_.struct])
                else:
                    coeff, var = self_.__extract__
                    other_ = 1
                    if '/' in format(self_):
                        mul_ = {}
                        div = True
                        for var_, pows in var.items():
                            if getter(var_, 'name') in ('Expr', 'Fraction'):
                                if div and '/' in format(var_):
                                    after_div = (coeff * var_) / other
                                    if '/' not in format(after_div):
                                        other_ *= after_div
                                    else:
                                        mul_[after_div] = pows
                                    div = False
                                else:
                                    mul_[var_] = pows
                            else:
                                mul_[var_] = pows
                        return Expr({1: [mul_]}) * other_
                    else:
                        return Expr({1: [{Frac(Expr({coeff: [var]}), other): 1}]})

            Quo = self_.new
            count = 0
            expect = self_.deg + 1 - other.deg
            var_test = self_.like(other)
            fomr = format(self_)

            while True:
                count += 1
                for i in range(1, len(other) + 1):
                    if not numable(other[i]) and self_.isdivisible(other[i]):
                        break
                otheri = other[i] / other[i]._coeff
                j = [self.pow(terms, otheri) for terms in self_]
                j = j.index(max(j)) + 1
                factor = self_[j] / other[i]
                sub = factor * other
                rem = (self_ - sub).simp()
                if not split and count > expect and rem:
                    return Expr({1: [{Frac(self, other): 1}]})
                Quo += factor
                if not round(rem, 14):
                    break
                if rem.deg < other.deg:
                    Quo += rem / other
                    break
                self_ = rem

            val = Quo

        return val.simp()

    def isfactor(self, factor):
        """
            Return True if factor is a factor of the Expression
        """
        factor = Expr(str(factor)) if getter(factor, 'name') != 'Expr' else factor
        if numable(factor):
            factor = num(factor)
            for coeffs in self.expr:
                if not intable(coeffs / factor):
                    return False
            return True
        if len(factor) > 1:
            raise InvalidOperation
        vars_ = factor.expr[factor._coeff][0]
        if len(vars_) > 1:
            for vars__, pows in vars_.items():
                if not self.isfactor(f'{vars__}^{pows}'):
                    return False
            return True
        x = list(vars_)[0]
        y = vars_[x]
        for exprs in self.struct:
            _vars_ = exprs.expr[exprs._coeff][0]
            if not x in _vars_:
                return False
            if _vars_[x] != y:
                return False
        return True

    def factor(self, factor):
        """
            Return True if divisible by factor
        """
        factor = Expr(str(factor)) if getter(factor, 'name') != 'Expr' else factor
        if numable(factor):
            return True
        if len(factor) > 1:
            raise InvalidOperation
        vars_ = factor.expr[factor._coeff][0]
        if len(vars_) > 1:
            for vars__ in vars_:
                if not self.factor(vars__):
                    return False
            return True
        x = list(vars_)[0]
        for exprs in self.struct:
            _vars_ = exprs.expr[exprs._coeff][0]
            if not x in _vars_:
                return False

        return True

    def isdivisible(self, other):
        """
            Return if no remainder will be returned after division
        """
        other = Expr(other)
        if len(other) > len(self):
            return False
        if numable(other) or len(other) == 1 or self == other:
            return True

        if len(other) > 1:
            for exprs in other:
                if numable(exprs):
                    continue
                div = []
                mun = 0
                for _exprs in self.struct:
                    if numable(_exprs):
                        mun += 1
                        continue
                    if _exprs.factor(exprs):
                        div.append(1)
                if len(div) >= len(self) - (mun + 1):
                    return True
        return False

    def coeff(self, other):
        """
            Return the coefficient of a variable in an Expression
        """
        coef = {}
        other_ = Expr(other)
        if list(other_.expr)[0] != 1:
            raise InvalidOperation
        coeff_, _var = other_.__extract__
        for exprs in self.struct:
            coeff, var = exprs.__extract__
            coef_ = list(other_.expr)[0]
            if all([(True if keys in var and var[keys] == values else False) for keys, values in _var.items()]):
                if coeff in coef:
                    coef[coeff].append({key: value for key, value in var.items() if not key in _var})
                else:
                    coef[coeff] = [{key: value for key, value in var.items() if not key in _var}]
        return Expr(coef).simp()

    def __complex__(self):
        """return the complex property of an Expr Object"""
        comp = self.new
        for exprs in self:
            if Expr(exprs).vars == ['j'] or Expr(exprs).isnum:
                comp += exprs
        comp = comp.simp()
        comp_ = comp[1].__str__()
        comp__ = comp[2].__str__()
        if comp__ != '-':
            comp__ = '+' + comp__
        if comp_ != '-':
            comp_ = '+' + comp_
        return complex((comp__ + comp_).replace(' ', ''))

    def isdivisible_(self, other):
        other = Expr(other) if not isinstance(other, Expr) else other
        for exprs in other.struct:
            if exprs.vars != self.like(exprs):
                return False
        return True


    def _isdivisible(self, other):
        other = Expr(other) if not isinstance(other, Expr) else other
        if not self.isdivisible(other):
            return False
        coeff = list(other.expr)[0]
        for _coeff in self.expr:
            if _coeff % coeff:
                return False
        return True

    @property
    def _coeff(self):
        """Return coefficient of a single term in an ExprObj"""
        if len(self) - 1:
            raise OperationNotAllowed
        return list(self.expr)[0]

    def __rtruediv__(self, other):
        return self.recreate(other) / self.recreate(self)

    @property
    def complex(self):
        """returns the complex part of an ExprObj"""
        comp = Expr({})
        for exprs in self.struct:
            if exprs.iscomplex:
                comp += exprs
        return comp.simp()

    @property
    def real(self):
        """returns the real part of an ExprObj"""
        comp = Expr({})
        for exprs in self.struct:
            if not exprs.iscomplex:
                comp += exprs
        return comp.simp()

    def __round__(self, other):
        """
            For approximations Use round(ExprObj, decimal places)
        """
        coeff = [round(coeff, other) for coeff in self.expr]
        vars_ = list(self.expr.values())
        rund = self.new
        for exprs in self.desolved.struct:
            crund = {}
            coeff, var = exprs.__extract__
            for var_, pows in var.items():
                if isinstance(var_, str):
                    crund[var_] = pows
                else:
                    var_ = round(var_, other)
                    if var_:
                        crund[var_] = pows
            if crund:
                rund += Expr({round(coeff, other): [crund]})

        return rund.simp()

    def __int__(self):
        """converts Expr Objects to Integers"""
        if not intable(self.__str__()):
            raise InvalidOperation(f"You can't take float of an expression {self}")

        return int(float(self))

    def __float__(self):
        """converts Expr Objects to Floats"""
        if not numable(self):
            raise InvalidOperation(f"You can't take float of an expression {self}")

        return float(str(self).replace(' ', ''))

    def __invert__(self):
        """Use ~ExprObj to find the reciprocal of ExprObj"""
        return 1 / self

    def __pow__(self, other):
        skip = False
        if isinstance(other, set):
            other = list(other)[0]
            skip = True

        other = alnum(other)
        if not other:
            return Expr('1')
        if other == 1: return self
        lenn = True if len(self) == 1 else False
        if lenn:
            coeff, var = self.__extract__
            s_var = list(var)[0]
        if numable(self, other):
            if format(other).endswith('.5') and num(self) < 0:
                return Expr('.i') ** (other * 2) * Expr(f'{abs(num(self)) ** other}', skip=skip)
            return Expr(f'{num(self) ** num(other)}', skip=skip)
        elif self.iscomplex and lenn and intable(other):
            self_ = self.duplicate()
            var = self_.expr[coeff][0]
            compl = 'î' if 'î' in var else 'ĵ' if 'ĵ' in var else 'ǩ'
            pow_ = var.pop(compl) * int(other)
            powc = abs(pow_)
            if powc >= 4: powc %= 4
            complc = Expr(compl) if powc == 1 else -1 if powc == 2 else -Expr(compl) if powc == 3 else 1
            if pow_ < 0: complc = complc if isinstance(complc, int) else -complc
            return ((Expr({coeff: [var]}) if var else coeff) ** other) * complc

        if isinstance(other, float) or not numable(other):
            if numable(self) and numable(other):
                return Expr(str(eval(f'num({self}) ** {other}')), skip=skip)
            else:
                result = 1
                if not isinstance(other, float) and len(other) > 1:
                    for index in other.struct:
                        result *= self ** index
                    return result

                if isinstance(other, float) and lenn:
                    if len(var) > 1:
                        return Expr({self._coeff ** other: [{Expr({1: [var]}): other}]})
                    pow__ = var[s_var] * other
                    return Expr({num(self._coeff ** other): [{s_var: pow__}]})

                return Expr({1: [{self: other}]})

        if lenn:
            pow__ = var[s_var] * other
            if getter(s_var, 'name') and intable(pow__) and len(var) == 1:
                return Expr(coeff ** other * s_var ** pow__)
        self_ = copy(self)
        for interger in range(abs(other) - 1):
            self_ *= self
        return self_ if other > 0 else Expr('1') if not other else ~self_

    def __rmul__(self, other):
        return self * other

    def __lt__(self, other):
        if not isinstance(other, Expr):
            other = Expr(f'{other}')
        a, b = alnum(self), alnum(other)
        return str(self) < str(other) if not isinstance(a, (int, float)) or not isinstance(a, (int, float)) else a < b

    def common(self, *exprs):
        common_list = []
        for expr in self.struct:
            for expr_ in exprs:
                if expr not in expr_:
                    break
            else:
                common_list.append(expr)
        return sum(common_list)

    def equate(self, expr):
        if not isinstance(expr, Expr):
            raise UnacceptableToken(f'{expr} must be a Expr Obj not {type(expr)}')
        working_set, values = com_arrays(self.vars, expr.vars), {}
        self_, expr_ = self, expr
        while True:
            reload = copy(values)
            for var in com_arrays(self.vars, expr.vars):
                common_ = self_.common(expr_)
                self_, expr_ = (self_ - common_).simp(), (expr_ - common_).simp()
                if var in str(self_.power_list()) and var in str(expr_.power_list()):
                    from engpy.misc.fragments import fragment_1
                    power_1, power_2 = fragment_1(self_, var), fragment_1(expr_, var)
                    try:
                        if power_1[1] != power_2[1] or '-' in f'{power_1[0] * power_2[0]}':
                            raise Exception
                        new_expr = power_1[0] - power_2[0]
                        values[new_expr.vars[0]] = new_expr.solved()
                        working_set.remove(new_expr.vars[0])
                        continue
                    except Exception:
                        pass

                power_1, power_2 = self_.get_powers(var), expr_.get_powers(var)
                condition_1 = len(power_1) == len(power_2) == 1
                condition_2 = not(numable(power_1[0]) and numable(power_2[0])) if condition_1 else False
                condition_3 = self_.coeff(f'{var}^{power_1[0]}') == expr_.coeff(f'{var}^{power_2[0]}') if condition_2 else False
                if condition_3:
                    new_expr = power_1[0] - power_2[0]
                    values[new_expr.vars[0]] = new_expr.solved()
                    continue
                power, power_2 = set(power_1), set(power_2); power = power.union(power_2)
                for powers in power:
                    try:
                        new_expr = self_.coeff(f'{var}^{powers}') - expr_.coeff(f'{var}^{powers}')
                        values[new_expr.vars[0]] = new_expr.solved()
                    except Exception:
                        pass

            if reload != values:
                self_, expr_ = self.cal(**values), expr.cal(**values)
                common_ = self_.common(expr_)
                self_, expr_ = (self_ - common_).simp(), (expr_ - common_).simp()
            if not working_set or reload == values:
                try:
                    new_expr = self_ - expr_
                    values[new_expr.vars[0]] = new_expr.solved()
                    working_set.remove(new_expr.vars[0])
                except Exception:
                    pass
                break
        return values

    def __gt__(self, other):
        if not isinstance(other, (Expr, int, float)):
            other = Expr(other)
        a, b = alnum(self), alnum(other)
        return str(self) > str(other) if not isinstance(a, (int, float)) or not isinstance(a, (int, float)) else a > b

    def solve(self, equate=0, rejection=True, fix='', **kwargs):
        """
            Solve Expr Objects when equals to the equate value

            if f(x) = 38x^4 - 127x^2 + 7x^3 - 21x + 39, Find the
            values of x for which f(x) = 0
            >>> fx = Expr('38x^4 - 127x^2 + 7x^3 - 21x + 39')
            >>> soln = fx.solve()
            To get the values, use next(soln)
            >>> next(soln)
            will yield 0.5
            the next function will keep on returning the values of x
            till StopIteration is raised when all the values of x
            has been returned

            Solve the Eqns
            cos(2θ) + cosec2(-3θ) - θ^2 - θ - 1 = 3tan2(2θ) - cot(θ)

            >>> eqn = Expr('cos(2theta)+cosec2(-3theta) - theta^2 - theta -1')
            >>> soln = eqn.solve('3tan2(2theta) - cot(theta)')
            >>> next(soln)
            This should yield 0.9748222067356423

            if only one solution is needed use solved method instead
            it accepts the same arguments as solve
            f(x) = (x + sin(x))/(1+cos(x)) and g(x) = 1/sin(x)

            Find  a value for x at which f(x) = g(x)

            >>> fx = Expr('(x + sin(x))/(1+cos(x))')
            >>> gx = Expr('1/sin(x)')
            >>> x = fx.solved(gx)

            x has a value of 0.9970497122338364

            Some Expressions need some reforming so as to be solved, which
            give rise to extraneous roots, by default the rejection arg has been
            set to True to reject all extraneous solutions

            Solve the equation 1/x + 1/sqrt( - x^2 + 10) = 4/3
            To get all the solutions
            >>> eqn = Expr('1/x + 1/sqrt( - x^2 + 10)')
            >>> all_soln = eqn.solve(4/3,rejection = False)
            >>> while True:
                    try:
                        print(next(all_soln))
                    except StopIteration:
                        break
            4 solutions are printed which are 1, 3, 0.6040496217739162, -3.104049621773916
            Because this is radical expression, the reform method may have been called at some
            point thereby rewriting the expression, so it's likely one or more of those solutions
            extraneous root.

            let's plug in the solutions to find out the extraneous roots.
            since we are finding the value of eqn for different values of x we use tables
            >>> eqn.tables((-3.104049621773916, 1, 3, 0.6040496217739162))
            which result in
            {-3.104049621773916: 4/3, 1: 4/3, 3: 4/3, 0.6040496217739162: 1937469/979681}
            it's clear that 0.6040496217739162 is an extraneous root as it doesn't agree with eqn

            By default the rejection is already set to True to reject extraneous
            solutions.

            >>> all_soln = Expr('1/x + 1/sqrt( - x^2 + 10)').solve(4/3)
            >>> while True:
                    try:
                        print(next(all_soln))
                    except StopIteration:
                        break

            The results are 1, 3, - 3.104049621773916
            The solution 0.604049621773916 has been removed


        """
        if not self.vars:
            raise InvalidOperation(f'No Unknown to Solve for in {self}')
        self_ = self - equate
        if kwargs:
            self_ = self_.cal(kwargs)
            if not round(self_, 10):
                raise ActionDuplicationError(
                    f'The Expression {self} has already been satisfied by the given values {dstar(kwargs)}')
        var_list = self_.vars
        if not var_list:
            raise InvalidOperation(f'No Unknown to Solve for in {self}')
        if len(var_list) == 1:
            var = var_list[0]

        if len(var_list) > 1:
            raise InvalidOperation(f'This Expression {self_} contains more than one unknowns')
        eqq = True
        reform = False
        standings = False
        onset = None
        useonset = False
        div = True

        if self_.iscomplex:
            try:
                root = self_.subject(var)
                standings = True
            except Exception:
                pass
        while True:

            try:

                root = New_Raph(self_, var) if not standings and not useonset else root
                standings = False
                if not intable(root) and numable(root):
                    run5 = str(Fraction(num(root)).limit_denominator())
                    if not '/' in run5:
                        root = num(run5)
                        root_ = root
                    elif len(run5) <= 7:
                        root = eval(run5)
                        root_ = root
                    else:
                        root_ = root
                else:
                    root_ = root
                _root = num(root_) if numable(root_) else root_
                toreturn = round(_root, fix) if fix else _root
                if rejection and reform:
                    in_put = self.cal({var: toreturn})
                    if not (in_put - equate > 0.000001 or in_put - equate < - .000001):
                        yield toreturn
                else:
                    yield toreturn
                if getter(root, 'name') == 'Expr' and root.iscomplex:
                    if not div:
                        useonset = True
                    root = root.conjugate
                    standings = True
                    if self_.deg == 2:
                        div = False
                if div:
                    self_ /= Expr(var) - root
                    self_ = sum([exprs for exprs in self_.struct if round(exprs, 10)])
                if useonset or not self_ or self_.isnum:
                    break
            except ZeroDivisionError:
                if reform:
                    if onset is not None:
                        useonset = True
                    else:
                        break
                try:
                    self_ = self_.reform()
                except InvalidOperation:
                    self_ = self.reform()
                reform = True
            except OperationNotAllowed:
                if reform:
                    if onset is not None:
                        useonset = True
                    else:
                        break
                reform = True
                try:
                    self_ = self_.reform()
                except (ImprobableError, InvalidOperation) as e:
                    self_ = self.reform()
            except ImprobableError:
                try:
                    if onset is not None:
                        raise Exception
                    root = self_.subject(var)
                    standings = True
                except Exception:
                    if reform:
                        if onset is not None:
                            useonset = True
                        else:
                            if not eqq:
                                self_ = self.reform()
                                eqq = True
                            else:
                                break
                    else:
                        self_ = self_.reform()
                        reform = True
                        eqq = self_ == self
                        continue

    def solved(self, equate=0, fix='', **kwargs):
        try:
            return next(self.solve(equate, fix, **kwargs))
        except StopIteration:
            return None

    def __le__(self, other):
        return True if self == other else self < other

    def __ge__(self, other):
        return True if self == other else self > other

    def __hash__(self):
        sstr = iformat(self)
        ll = list(range(1, len(sstr) + 1))
        ash = 1
        for count, char in enumerate(sstr):
            ash *= char.index(char) * ll[count]
            ash += 3
        return ash % 10000000000

    @property
    def vectorized(self):
        return True if self.iscomplex else False

    def __mul__(self, other):
        if getter(other, 'name') == 'Vector':
            return other * self
        skip = ''
        FF = format(self)
        OO = format(other)
        if (isinstance(other, str) or getter(other, 'name') == 'Expr') and ('.F' in OO or 'Ƒ' in OO):
            other = OO.replace('.F', 'Ƒ')
            ind = other.index('Ƒ')
            _var = []
            ind += 1
            while ind < len(other):
                _var.append(other[ind])
                ind += 1
            __var = _var
            if len(__var) == 1:
                __var = _var[0]
            if not _var:
                __var = 'x'
            vars_ = "".join(_var)
            return (Expr(other.replace(f'Ƒ{vars_}', '') if other.replace(f'Ƒ{vars_}', '') else '1') * self.lin_diff(
                __var)).simp()
        elif 'Ƒ' in FF:
            return other * self
        if numable(other):
            other = Expr(other)
        if isinstance(other, (str, int32, complex)):  # Ensuring that we are dealing with Expr object
            other = Expr(OO)
        elif getter(other, 'name') in ('trig', 'log', 'Fraction'):
            other = Expr(other)

        elif getter(other, 'name') == 'Expr':
            pass
        elif isinstance(other, set):
            other = Expr(other)
            skip = 1
        else:
            raise KindError(f'{type(other)} is not supported')
        fracs = {}
        other = other.simp(desolve='')
        if '/' in FF:
            for part in self.struct:
                if not '/' in format(part):
                    continue
                den = get_den(part)[0]
                if other.isdivisible(den):
                    quo = other / den
                    if '/' in format(quo):
                        continue
                    cf, part = part.__extract__
                    if len(part) > 1 and '' in part:
                        part.pop('')
                    if getter(list(part)[0], 'name') == 'Expr':
                        p_art = list(part)[0]
                        cf_, p_art = p_art.__extract__
                        cf *= cf_
                    else:
                        p_art = part
                    fracs.update({str(part): cf * quo * list(p_art)[0].num})
                    continue
                if (len(other) == 1 and den.isfactor(other)) or (len(other) > 1 and den.isdivisible(other)):
                    quo = den / other
                    if '/' in format(quo):
                        continue
                    cf, part = part.__extract__
                    if len(part) > 1 and '' in part:
                        part.pop('')
                    if getter(list(part)[0], 'name') == 'Expr':
                        p_art = list(part)[0]
                        cf_, p_art = p_art.__extract__
                        cf *= cf_
                    else:
                        p_art = part
                    fracs.update({str(part): (cf * list(p_art)[0].num) / quo})

        elif '/' in OO:
            return other * self

        sef_ = {}
        val_ = {}
        _val_ = []
        statr = 0

        if not self or not other:
            return Expr('')
        once = True if numable(other) else False

        for __exprs__ in other.struct:

            coeff, var = __exprs__.__extract__
            sef = {coeff__ * coeff: var_ for coeff__, var_ in self.expr.items()}

            if once:
                return Expr(sef)
            _sef_ = self.new
            for _coeff, vas in sef.items():
                vars_ = []
                if fracs:
                    for vas_ in vas:
                        if str(vas_) not in fracs:
                            vars_.append(vas_)
                else:
                    vars_ = vas
                if not vars_:
                    continue

                for vars__ in vars_:
                    for _vars__, pow_ in vars__.items():
                        if _vars__ in var:
                            val_[_vars__] = alnum(pow_ + var[_vars__])

                        else:
                            val_[_vars__] = pow_

                        for __vars__ in var:
                            if __vars__ not in val_:
                                val_[__vars__] = var[__vars__]
                    _val_.append(val_)
                    val_ = {}
                _sef_.expr[_coeff] = _val_
                _val_ = []
            if not statr:
                add = _sef_
            else:
                add += {_sef_} if skip else _sef_

            statr += 1
        for index, items in fracs.items():
            add += {items} if skip else items
        return add.simp() if statr else self.new

    @property
    def _iscomplex(self):
        """return True for numbers and complex components"""

        var_list = self.variables
        if not var_list:
            return False
        for restrict in complex_id:
            if restrict in var_list:
                return True
        return False

    @property
    def iscomplex(self):
        """return True only if complex identities are present"""
        return check_rest(complex_id, self.variables)

    def __bool__(self):
        """returns bool(ExprObj)
            works with if statement
            Any Expr Object that is not 0 will return True else False

            f(x) = 2x^2 - 8x + 8, g(x) = x - 2;
            If h(x) = f(x) - 2 * g(x)^2, Prove that h(x) is a Zero/empty

            >>> fx = Expr('2x^2 - 8x - 8')
            >>> gx = Expr('x - 2')
            >>> if fx and gx:
                    hx = (fx - 2 * gx ** 2).simp()
                if hx:
                    print('False, h(x) is not a Zero')
                else:
                    print('True, h(x) is a Zero function')
        """
        if not self.expr:
            return False
        for coeffs in self.expr:
            if not coeffs:
                return False
        return True

    def __copy__(self, s=''):
        return copy(self)

    def __deepcopy__(self, s=''):
        return deepcopy(self)

    def __neg__(self):
        return -1 * self

    def index(self, args):
        """return the index of a term in an ExprObj"""
        index_ = 0
        for exprs in self:
            index_ += 1
            if exprs.replace(' ', '') == str(args).replace(' ', ''):
                return index_
        raise QueryError(f'{args} not present')

    def __rpow__(self, other):

        return Expr(other) ** self

    @property
    def cleared(self):
        """Clear all terms in the Expr Object to Zero"""
        self.expr = {0: [{'': 0}]}

    @property
    def conjugate(self):
        """return the conjugate of an ExprObj,
            This Property asserts that the ExprObj contains complex identities
            else an exception is raised
        """
        if not self._iscomplex:
            raise InvalidOperation('Only Complex Numbers has Conjugate Pairs')

        con = self.new
        for exprs in self.struct:
            if exprs.iscomplex:
                con -= exprs
                continue
            con += exprs

        return con.simp()

    def parse(self):
        new_expr = {}
        for expr in self.struct:
            for coeff, var in expr.expr.items():
                for var_ in var[0]:
                    new_expr[var_] = coeff
        return new_expr

    def split(self, var=''):
        """
            This method breaks Expr Objects into two fragments
            it collect all terms with var arguments and separate it
            and return the fragemts in a tuple

            y = 3xcos2(2t) - cot(t)sec2(t) + x^2t - 6plog2x(5x) + 2
            To separate terms with x from the expression

            >>> y = Expr('3xcos2(2t) - cot(t)sec2(t) + x^2t - 6ploga(5p) + 2')
            >>> y.split('x')
            which yield ( - cot(t)sec2(t) + 2, 3xcos2(2t) + x^2t - 6plog2x(5p))

            To match more than one parameter, use list or tuple instead
            for example to match terms with x and terms with p
            >>> y.split(('x', 't'))
            which yield ( - 6ploga(5p) + 2, 3xcos2(2t) + x^2t - cot(t)sec2(t))

            To match terms with more than one aparameter simultaneously, use set
            for example to match terms has both  x and t
            >>> y.split({'x', 't'})
            which yield ( - cot(t)sec2(t) - 6ploga(5p) + 2, 3xcos2(2t) + x^2t)
        """
        if isinstance(var, str):
            for greeks in greek_map:
                if not greeks in ('eta', 'Eta'):
                    var = var.replace(greeks, greek_map[greeks])
        if isinstance(var, (list, tuple)):
            res_ = []
            res = []
            done = []
            stack = ''
            for _var in var:
                if not _var:
                    continue
                if _var in done:
                    continue
                if stack == 0:
                    continue
                v_list = (self if not stack else stack).split(_var)
                res += [v_list[0]]
                res_ += [v_list[1]]
                done.append(_var)
                stack = sum(res)
            return tuple([mix(res)] + [sum(res_)])
        if not var:
            return [self]
        res = self.new
        res_ = self.new

        if isinstance(var, set) and var:
            for exprs in self.struct:
                exprs_ = format(exprs)
                match = 1
                for var_ in var:
                    if not var_ in exprs_:
                        match = 0
                        break
                if match:
                    res += exprs
                else:
                    res_ += exprs
            return res_, res

        if len(self) > 1:
            for exprs in self.struct:
                if var.replace(' ', '') in format(exprs).replace(' ', ''):
                    res += exprs
                else:
                    res_ += exprs
            return res_, res

        coeff = self._coeff
        _var = self.expr[coeff][0]
        for var_ in copy(_var):
            if var in str(var_).replace(' ', '') or var.replace(' ', '') in str(_var[var_]).replace(' ', ''):
                res += f'{var_} ^ {_var[var_]}'
                _var.pop(var_)
        return Expr({coeff: [_var]}), res

    def duplicate(self):
        return Expr(deepcopy(self.expr))

    def wraps(self, var, detailed=False):
        """returns True an expression or variable is present
        Similar to the "in" keyword, but here the coefficients are ignored
        passing the arg detailed as True returns the exact match in a tuple
        """
        var = Expr(var)
        c_list = []
        dtail = []
        for vars_ in var.struct:
            coeff, v_var = vars_.__extract__
            for w, exprs in enumerate(self.struct):
                if w in c_list:
                    continue
                coeff, _exprs = exprs.__extract__
                n = len(c_list)
                for terms, pows in v_var.items():
                    try:
                        if len(_exprs) != len(v_var) or _exprs[terms] != pows:
                            break
                        c_list.append(w)

                    except KeyError:
                        break
                else:
                    break
            else:
                return False
            if detailed:
                dtail.append(exprs)
        return tuple(dtail) if detailed else True

    def __eq__(self, other):
        """Supports comparision"""
        other = Expr(other)

        self_ = self.simp()
        other = other.simp()
        for exprs in other.struct:
            if not exprs in self_:
                return False
        return True if not len(other) - len(self_) or format(self) == format(other) == '0' else False

    def solns(self, equate=0, repeat=False, rejection=True, fix='', **kwargs):
        """This return all the solutions in a tuple"""
        '''By default the repeat arg is False, so repeated roots/solutions are ignored,
          setting repeat to True will return all repeated solutions.'''
        soln = tuple(self.solve(equate, rejection, fix, **kwargs)) if repeat else tuple(
            set(self.solve(equate, rejection, fix, **kwargs)))
        return soln if soln else None

    def __ne__(self, other):
        return not self == other

    def __format__(self, q):
        return self.__str__(d=0)


Es = Expr('!@#$%^', True)


class Eqn:
    def __init__(self, LHS, RHS):
        self.name = 'Eqn'
        self.LHS = Expr(LHS)
        self.RHS = Expr(RHS)

    def __str__(self):
        return repr(self.LHS) + ' = ' + repr(self.RHS)

    @property
    def crossed(self):
        self.LHS -= self.RHS
        self.LHS = self.LHS.simp()
        self.RHS.cleared

    @property
    def vars(self):
        return tuple(list(self.LHS.vars) + list(self.RHS.vars))

    @property
    def Lcrossed(self):
        self.RHS -= self.LHS
        self.RHS = self.RHS.simp()
        self.LHS.cleared

    @property
    def islinear(self):
        return self.RHS.islinear and self.LHS.islinear

    def __eq__(self, other):
        if getter(other, 'name') == 'Eqn':
            other = other.LHS - other.RHS
        return self.LHS - self.RHS == other

    @property
    def swap(self):
        r = self.LHS
        self.LHS = self.RHS
        self.RHS = r

    def cross(self):
        return (self.LHS - self.RHS).simp()

    __repr__ = __str__


class Eqns(ExpressionObjectClass):
    import arrays.matrix as arm
    def __init__(self, *expr, norm=False, segregate=False):
        self.name = 'Eqns'
        self.list = []
        self.norm = norm
        self.segregate = segregate
        for exprs in expr:
            if isinstance(exprs, str) and ',' in exprs:
                exprs = exprs.split(',')
                for exprs_ in exprs:
                    self.add(exprs_)
                continue

            self.add(exprs)

    def add(self, *eqns_, append=True):
        for eqn in eqns_:
            if isinstance(eqn, str):
                eqn = eqn.split('=')
                if len(eqn) == 1:
                    eq = Expr(0)
                else:
                    eq = Expr(eqn[1])
                eqn = Expr(eqn[0])
            elif getter(eqn, 'name') == 'Expr':
                eqn = eqn.simp()
                eq = Expr(0)
            elif getter(eqn, 'name') == 'Eqn':
                eqn, eq = eqn.LHS, eqn.RHS
            if not self.norm:
                if not append:
                    return Eqn(eqn, eq)
                self.list.append(Eqn(eqn, eq))
            else:
                if not append:
                    return (eqn - eq).simp()
                self.list.append((eqn - eq).simp())

    def __str__(self):
        return '\n'.join([repr(self[i]) for i in range(1, len(self) + 1)])

    def __len__(self):
        return len(self.list)

    @property
    def vars(self):
        var_list = []
        for eqns in self:
            var_list += eqns.vars
        return sorted(set(var_list))

    def visualize(self, color='', linewidth=2, *args, **kwarg):
        self_ = self.cross()
        var_list = list(self.vars)
        if len(var_list) > 2:
            raise OperationNotAllowed

        var_list += [rev(greek_map)[greeks] for greeks in var_list if greeks in rev(greek_map)]
        var = {}
        kwargs = {}

        for keys, values in kwarg.items():
            if keys in var_list:
                values.step = .05
                var.update({keys: list(values)})

            else:
                kwargs.update({keys: values})
        sec_var = ''
        if len(var_list) == 2:
            var_list.remove(keys)
            sec_var = var_list[0]

        return Visualize(var, self, color, sec_var, linewidth, *args, **kwargs).multiplot

    def solve(self, matrix='', vmat='', option='all', generator=False, **kwargs):
        if not matrix:
            self_ = self.cross()
            gvar_list = self_.vars
        else:
            gvar_list = vmat
        usvar = ''

        def matrix_rays():
            from engpy.arrays import Matrix_
            nonlocal self_, gvar_list, xtra, usvar, matrix
            if not matrix and not self_.islinear:
                return None
            rays, equate = [], []
            if not matrix:
                for eqns in self_:
                    rays += [eqns.coeff(var) for var in gvar_list]
                    rays.append(-eqns.const)
                rays = Matrix_([len(self), len(gvar_list) + 1] + rays)
            else:
                rays = matrix.__copy__()
            reduced = rays.echelon()
            res = reduced.pop('-1')
            col_vec, gvar = reduced * Matrix_([len(gvar_list), 1] + gvar_list), copy(gvar_list)
            col_vec.reverse()
            gvar.reverse()
            res.reverse()
            _score = 1
            resolve = Eqns()
            usvar = 'k'
            for elements, var, eq in imap(col_vec.elements, gvar, res):
                if var is None:
                    break
                if not elements or not elements.coeff(var):
                    add_soln({var: [[Expr(f'k{_score}')]]})
                    _score += 1
                else:
                    if elements.vars == [var]:
                        add_soln({var: [[(elements - eq).subject(var)]]})
                    else:
                        resolve.add(Eqn(elements, eq))

            self_ = resolve.cross()
            reset()
            substitute()

        es = ''

        def add_soln(soln, mode='ins'):
            nonlocal xtra
            if len(soln) > 1:
                for sols, lis in soln.items():
                    add_soln({sols: lis})
                return
            out = False
            ashift = 0
            varr = list(soln)[0]
            if not xtra:
                xtra[varr] = soln[varr][0]
                out = True
            if varr not in xtra:
                xtra[varr] = []
            for i, vals in enumerate(soln[varr]):
                if out:
                    break
                i -= ashift
                v = len(vals)
                i *= v
                for sec, variablee in enumerate(xtra):
                    if variablee == varr:
                        if mode == 'ins':
                            break

                    for v_, vs in enumerate(vals):
                        if vs is None:
                            del xtra[variablee][i]
                            ashift += 1
                            break
                        if mode == 'ins' and v_:
                            xtra[variablee].insert(i, xtra[variablee][i])
                        if not sec:
                            xtra[varr].append(vs)
                    else:
                        if not vals:
                            xtra[varr].append(None)
                    if mode != 'ins':
                        break

        def _draw():
            nonlocal xtra
            if xtra:
                for i in range(len(list(xtra.values())[0])):
                    yield {var: values[i] for var, values in xtra.items()}

        def draw():
            nonlocal es
            if not es:
                es = _draw()
            try:
                return next(es)
            except StopIteration:
                return None

        def solution():
            nonlocal xtra
            solns, tested = {}, []
            while True:
                values = draw()
                if values is None: break
                try:
                    if str(values) in tested:
                        continue
                    if not self.segregate:
                        self.verify(values)
                    tested.append(str(values))
                except (ConcurrenceError, ZeroDivisionError) as e:
                    pass
                else:
                    for var, vals in dict(sorted(list(values.items()), key=lambda d: d[0])).items():
                        if not var in solns:
                            solns[var] = []
                        solns[var].append(vals)
            xtra = solns
            return _draw() if generator else list(_draw())

        def reset():
            nonlocal subject, current, es, solns_
            subject, current, es, solns_ = None, 0, '', ''

        def Pick(mode=True):
            nonlocal self_
            min_lis = []
            for n, eqns in enumerate(self_, 1):
                if '/' in format(eqns):
                    self_[n] = eqns.reform()
                min_lis.append((n, eqns, len(eqns)))
            min_lis = sorted(min_lis, key=lambda ms: ms[2])

            if not mode:
                yield min_lis
            for n, eqns, c in min_lis:
                for terms in eqns.struct:
                    for e, eqns_, c in min_lis:
                        if e == n:
                            continue
                        warp = eqns_.wraps(terms, True)
                        if warp:
                            yield n, e, terms._coeff, warp[0]._coeff
            yield None

        def eliminate():
            nonlocal self_, gvar_list, elm
            for countss in range(len(self_) + 1):
                self_[countss] = self_[countss].reform()
            pck = Pick()
            while True:
                strand = next(pck)
                if strand is None:
                    break
                try:
                    multiplier = Num([strand[2], strand[3]]).LCM()
                except TypeError:
                    multiplier = strand[2] * strand[3]
                eqn1 = self_[strand[0]] * multiplier / strand[2]
                eqn2 = self_[strand[1]] * multiplier / strand[3]
                self_.insert((eqn1 - eqn2).simp(), elm)
                elm += 1
                break

        def pick(s=0):
            nonlocal self_, current
            lenv = []
            for cn, eqn in enumerate(self_, 1):
                if cn == current:
                    continue
                v = eqn.vars
                if s:
                    po = 0
                    for vs in v:
                        try:
                            po += eqn.powof(vs)
                        except QueryError:
                            po += 0
                    lenv.append((cn, len(v), po))
                else:
                    lenv.append((cn, len(v)))
            if s:
                return sorted(lenv, key=lambda lenvs: lenvs[2], reverse=True)
            return sorted(lenv, key=lambda lenvs: lenvs[1])

        def solve():
            nonlocal self_
            for n, eqns in enumerate(self_, 1):
                if option in ('all', n) or option == n:
                    add_soln({eqns.vars[0]: [[eqns.solns(**kwargs)]]}, 1)
            return solution()

        def substitute():
            nonlocal es, solns, self, eqns, current, subject, xtra, usvar, gvar_list, w_var
            lenv = pick(1)
            next_ = False
            _shift = 0
            for ind, len_, non in lenv:
                after = True
                solns_ = []
                ind -= _shift
                while True:
                    if not next_:
                        vales = draw()
                    next_ = False
                    if vales is None:
                        if subject is None:
                            es = ''
                            break
                        vales = subject
                    if subject and w_var not in self_[ind].vars:
                        break
                    eqn = self_[ind].cal(vales)
                    if not eqn:
                        for v in self_[ind].vars:
                            if v not in xtra:
                                break
                        else:
                            del self_[ind]
                            _shift += 1
                            next_ = True
                            break
                    var__ = eqn.vars
                    icount = 0
                    if len(var__) > 1 and usvar:
                        for v_ar in var__:
                            if not usvar in v_ar:
                                _svar = v_ar
                                icount += 1
                    if len(var__) == 1 or icount == 1:
                        if icount == 1:
                            _solns = [eqn.subject(_svar)]

                        else:
                            _svar = var__[0]
                            _solns = eqn.solns(rejection=False)

                        if _solns is not None:
                            solns_.append(list(_solns))

                        else:
                            del self_[ind]
                            _shift += 1
                            break
                    elif not var__:
                        if xtra:
                            solns_.append([None])
                        else:
                            del self_[ind]
                            _shift += 1


                    elif self_[ind] != eqn:
                        self_[ind] = eqn
                        next_ = True
                        break
                    elif self_[ind] == eqn:
                        next_ = True
                        break
                    if not xtra:
                        break
                if next_:
                    continue
                if solns_:
                    del self_[ind]
                    _shift += 1

                if solns_:
                    for items in solns_:
                        if items[0] is not None:
                            break
                    else:
                        continue
                    add_soln({_svar: solns_})
                    reset()
                    if len(xtra) == len(gvar_list):
                        return solution()
                    else:
                        return substitute()
            subject = None

        solns_ = ''
        counter = 0
        current = None
        solns = {}
        subject = ''
        xtra = {}
        shift = 0
        elm = 1
        if matrix or self_.islinear:
            matrix_rays()
            if len(xtra) == len(gvar_list):
                reset()
                return solution()
        while subject is not None:
            if self.segregate:
                return solve()
            if counter == len(self.vars) * len(self):
                return None
            counter += 1
            subject = None
            restart = False
            shift = 0
            for current, p in pick():
                try:
                    eqns = self_[current]
                except OutOfRange:
                    subject = ''
                    break
                v_list = eqns.vars
                if len(v_list) == 1 and v_list[0] not in xtra:
                    subject = eqns.solns(rejection=False)
                    del self_[current]
                    shift += 1
                    add_soln({v_list[0]: [list(subject)]}, '')
                    subject = None
                    reset()
                    pause = substitute()
                    if pause is not None:
                        return pause
                else:
                    if len(v_list) > 1:
                        vlist = [letter for letter in v_list if letter not in solns]
                        if not xtra:
                            for variable in gvar_list:
                                ind = eqns.get_power(variable)
                                if ind and not isinstance(ind, list):
                                    w_var = variable
                                    try:
                                        subject = {variable: eqns.subject(variable)}
                                    except (OperationNotAllowed, InvalidOperation) as e:
                                        continue
                                    pause = substitute()
                                    if pause is not None:
                                        return pause
                                    else:
                                        restart = True
                                        subject = True
                                        break
                            if restart:
                                break

                        if len(vlist) == 1:
                            subject = eqns.subject(v_list[0])
                            solns[v_list[0]] = subject
                if len(gvar_list) == len(solns):
                    xtra = solns
                    return solution()
            else:
                eliminate()
                subject = ''

    def __delitem__(self, other):
        del self.list[other - 1]

    def insert(self, other, index):
        other = self.add(other, append=False)
        self.list.insert(index - 1, other)

    def pop(self, index):
        item = self[index]
        del self[index]
        return item

    def __eq__(self, other):
        if getter(other, 'name') != 'Eqns':
            raise UnacceptableToken(f'Only two Eqns Objects can be compared not {type(other)}')
        checklist = []
        if len(self) != len(other):
            return False
        for eqns in self:
            for n, eqn in enumerate(other):
                if n in checklist:
                    continue
                if eqns == eqn:
                    checklist.append(n)
        return len(self) == len(checklist)

    def verify(self, values='', **kwargs):
        if isinstance(values, (list, tuple)):
            for value in values:
                kwargs.update(value)
                self.verify(**kwargs)
            return None
        elif values:
            if not isinstance(values, dict) and len(self.vars) == 1:
                kwargs.update({self.var[0]: values})
            elif isinstance(values, dict):
                kwargs.update(values)
            elif not kwargs:
                raise Vague('Request not understood')
        for n, eqns in enumerate(self, 1):
            if not self.norm:
                if round((eqns.LHS - eqns.RHS).cal(**kwargs, desolved=True), 10):
                    raise ConcurrenceError(f"The Solution {dstar(kwargs)} is not satisfied by eqn {n}: {eqns}")
            else:
                if round(eqns.cal(**kwargs, desolved=True), 10):
                    raise ConcurrenceError(f"The Solution {dstar(kwargs)} is not satisfied by eqn {n}: {eqns}")

    def cross(self):
        return Eqns(*[eqns.cross() for eqns in self], norm=True)

    def __getitem__(self, other):
        return self.list[other - 1]

    @property
    def islinear(self):
        for eqn in self:
            if not eqn.islin:
                return False
        return True

    def __setitem__(self, other, value):
        self.list[other - 1] = value.simp() if getter(value, 'name') == 'Expr' else Expr(value).simp()

    class Eqns_iter:
        def __init__(self, eqn):
            self.eqn = eqn
            self.it = self.get()

        def get(self):
            for nomb in range(1, len(self.eqn) + 1):
                yield self.eqn[nomb]

        def __next__(self):
            return next(self.it)

        def __iter__(self):
            return self

    def __iter__(self):
        return self.Eqns_iter(self)

    def __copy__(self):
        return deepcopy(self)

    __repr__ = __str__


call = False
EsQ = Eqns()


def main():
    global call
    call = True


if __name__ == '__name__':
    main()
