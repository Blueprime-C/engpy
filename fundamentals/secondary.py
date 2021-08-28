from misc.abilities import numable
from misc.miscs import num
from errors.exceptions import OperationNotAllowed

from .primary import break_pq, count_powers

from .assorted import C, CD, GCD
from misc.imports import create
from misc.abilities import intable
from Standard import stdlib
from Standard.stdlib import Numbers
from misc.internals import check_coeff_ind, unnest


def pascal(index):
    return [C(index, base) for base in range(index + 1)]


def group_factor(expr, strict=True, proofing=False):
    exprs = list(expr.struct)
    step, grouped, used, factor_grouped, even, proof = 0, [], [], [], not bool(len(exprs) % 2), False
    for i in range(len(exprs)):
        if i + 1 in used: continue
        used.append(i + 1); common, number_factants = [exprs[i]], 1
        for count, exprs_ in enumerate(exprs, 1):
            if count in used: continue
            if CD(True, *(common + [exprs_])):
                common.append(exprs_)
                used.append(count)
                number_factants, proof = number_factants + 1, True
            if strict and even and number_factants >= len(exprs)/2: break
        grouped.append(sum(common))
    if not proof: return None
    for groups in grouped:
        rrr = groups.factorize() if len(groups) > 1 else groups
        factor_grouped.append(rrr)
    return sum(factor_grouped)


def difference_powers(expr):
    func = create(expr)
    work, skip, remain, temp, powers_2, powers_3 = {}, [], func({}), [], {}, {}
    for exprs in expr.struct:
        coeff, terms = exprs.__extract__
        power_list = GCD(*list(terms.values()))
        if not power_list % 2:
            if abs(coeff) not in powers_2: powers_2[abs(coeff)] = []
            powers_2[abs(coeff)].append(exprs/abs(coeff))
        elif not power_list % 3:
            if abs(coeff) not in powers_3: powers_3[abs(coeff)] = []
            powers_3[abs(coeff)].append(exprs / abs(coeff))
        else:
            remain += exprs
    work[2] = powers_2; work[3] = powers_3
    for key, list_ in work.items():
        sign = None
        for coeffs, terms in list_.items():
            nn = 0; cancel = True
            while nn < len(terms):
                term = terms[nn]
                if term._coeff < 0: sign = True
                else: sign = False
                if not temp or (sign == False and temp) or (sign is None and temp): temp.append(term)
                if len(temp) == 2:
                    term_1, term_2, nn, cancel = temp, -1, True; terms.remove(term_1); terms.remove(term_2)
                    if sign:
                        remain += func({coeffs: [{term_1 ** (1 / key) + stdlib.abs(term_2) ** (1 / key): 1,
                                                  term_1 ** (1 / key) - stdlib.abs(term_2) ** (1 / key): 1}]})
                    else:
                        remain += func({coeffs: [{term_2 ** (1/key) + stdlib.abs(term_1) ** (1/key): 1,
                                              term_2 ** (1/key) - stdlib.abs(term_1) ** (1/key): 1}]})

                    temp, sign, cancel = [], None, False

                nn += 1
                if nn == len(terms) and cancel:
                    remain += coeffs * sum([term for term in terms])
                    break
    return remain


def difference_powers(exprs, sep=False):
    func = create(exprs)
    expr, skip, factored, temp, powers_2, done, n, unfactored = exprs.recreate({}), [], func({}), [], [], [], 1, []
    exchange_done, figures = {}, []
    while n < len(exprs) + 1:
        exprs_ = exprs[n]
        c, f = check_coeff_ind(exprs_, True)
        if not f and numable(exprs_):
            figures.append(exprs_); n += 1
            continue
        if c and f:
            if intable(abs(c) ** (1/f)):
                c1, c2 = break_pq(c, f)
                expr += exprs.recreate({c1: [{(exprs_/c1) ** (1/f): f}]})
                powers_2.append(f)
            else: expr += exprs_
        else: expr += exprs_

        n += 1
    for figure in figures:
        for powers in powers_2:
            c1, c2 = break_pq(figure, powers)
            if c2 != 1:
                expr += exprs.recreate({c1: [{func(c2 ** (1 / powers)): powers}]})
            break
        else:
            expr += figure

    p_lines, target, additives = Numbers.reflected_planes(*list(expr.expr)), {}, []
    for terms in expr.struct:
        coeff, term = terms.__extract__
        term_ = terms / coeff
        if abs(coeff) in p_lines:
            power = GCD(*list(term.values()))
            index = 2 if not power % 2 else 3 if not power % 3 else 1
            if index != 1:
                term_ = func({1: [{term_ ** (1/index): index}]})
            if coeff not in target:
                target[coeff] = []
            target[coeff].append(term_); exchange_done[term_] = terms
    for lines in target:
        for term_1 in target[lines]:
            if term_1 < 0: continue
            power = GCD(*list(term_1.expr[1][0].values()))
            index = 2 if not power % 2 else 3 if not power % 3 else 1
            if index == 1:
                continue
            for term_2 in target[-lines]:

                if term_2 not in temp and not GCD(*list(term_2.expr[1][0].values())) % index:
                    temp += [term_1, term_2]; done += [exchange_done[term_1], exchange_done[term_2]]
                    term_1, term_2 = term_1 ** (1 / index), term_2 ** (1 / index)
                    term_1, term_2 = unnest(term_1), unnest(term_2)
                    if index == 3:
                        factored += func({lines: [{term_1 - term_2: 1, term_1 + term_2: 2}]})
                    else:
                        factored += func({lines: [{term_1 - term_2: 1, term_1 + term_2: 1}]})

                    break
    for terms in expr.struct:
        if not terms in done:
            try:
                unfactored.append(unnest(terms))
            except OperationNotAllowed:
                unfactored.append(terms)

    return (factored + sum(skip + unfactored)) if not sep else factored, sum(skip + unfactored)