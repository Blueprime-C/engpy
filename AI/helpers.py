from misc.vars import greeks, _alpha
from misc.assist import get_exprs


predefined_keywords = ['cos', 'sin',
                        'tan', 'cosh',
                        'sinh', 'e', '^',
                        'log', 'sec',
                        'cosec', 'cot'
                       ] + greeks


def get_key_word(string):
    n = 0; key_w = [];sub = ''
    while  n < len(string):
        if string[n] in _alpha:
            sub = ''; n += 1; continue
        if sub in predefined_keywords and sub + string[n] not in predefined_keywords:
            key_w.append(sub); sub = ''; n += 1; continue
        if string[n] not in ('(',')','+','-','*','/',' '):
            sub += string[n]
        n += 1
    if sub in predefined_keywords:
        key_w.append(sub)
    return set(key_w)


def score(string, exprs):
    exprs, string = exprs.replace(' ',''), string.replace(' ','')
    res = 0; con = 0; add = 0; exprs_ = list(exprs)
    tem = ''; n = '';exp_list, rule_list = [],[]
    for c, cahr in enumerate(string):
        if cahr in exprs_:
            if n != c and cahr == '(':
                if tem+'(' in exprs:
                    add += 1
                    rule = get_exprs(string, c)[0]
                    tem_ = []; v = exprs.index(tem+'(') + len(tem)
                    exp, c_ = get_exprs(exprs, v)
                    exprs = list(exprs)
                    for ch in exp:
                        try:
                            exprs.remove(ch)
                            exprs_.remove(ch)
                        except ValueError:
                            pass
                    exprs = ''.join(exprs)
                    tem_.append(exp)
                    exp_list.append(tuple(tem_)); tem_=[]
                    rule_list.append(rule);exp,rule = '',''; tem = ''
                    recazt = True
            add += 1 if con else 0
            if cahr != '(':
                exprs_.remove(cahr)
            res += add
            con = 1
            if cahr.isalpha():
                tem += cahr
        else:
            con = 0; tem = ''
    for i in range(len(exp_list)):
        rule_count = (rule_list[i].count('-'), rule_list[i].count('+'))
        get_len = [len(lenn) for lenn in exp_list[i]]
        j = get_len.index(max(get_len))
        

        exp_count = (exp_list[i][j].count('-'), exp_list[i][j].count('+'))
        s1,s2, x1,y1,x2,y2 = sum(exp_count), sum(rule_count), exp_count[0], exp_count[1], rule_count[0],rule_count[1]
        if s1 and s2 and x1 == x2 and y2 == y1:
            res += 3 + len(rule_list[i]) + len(rule_list[i])//2
        elif s1 and s2 and (x1 >= x2 or y1 >= y2):
            res += 2 + len(rule_list[i])
        elif not s1 and not s2:
            pass
        else:
            res -= 2 + len(rule_list[i])
    return res


def guage(string):
    prev = ''
    res = 0; add = 0; string = string.replace(' ',''); brac = 0
    for z in string:
        
        if (prev in ('','+','-','*','/') and z.isnumeric()) or brac:
            continue
        
        add += 1
        res += add
    return res


def weight(string,exprs):
    return guage(string)/score(exprs)
