from misc.assist import get_exprs


def scan_MD(expr, sign='', std='', state=''):
    if not sign:
        sign = '*'
    if sign not in expr:
        std = -1
    std = expr.index(sign) - 1 if not std else std - 1
    LHS = ''; brac = 0; sign = 0; std_ = std+2
    # Reading LHS
    while std > -1:
        if expr[std] == ')':
            brac += 1
        elif expr[std] == '(':
            if not brac:
                break
            brac -= 1
        if not brac and expr[std] in ('-','+','*','/'):
            if expr[std] == '-':
                LHS += expr[std]
            break
        LHS += expr[std]
        std -= 1
                
    LHS = list(LHS); LHS.reverse(); LHS = ''.join(LHS);LSH = LHS
    if LHS[0:2] == '-(':
        LHS = LHS.replace('-(','-1(')
    # Reading RHS
    RHS = ''; brac = 0; _std = std_
    while std_ < len(expr):
        if not (_std - std_) and expr[std_] == '(':
            RHS, std_ = get_exprs(expr,std_)
            continue
        elif expr[std_] == '(':
            rhs, std_ = get_exprs(expr,std_)
            RHS += rhs
            continue
        elif expr[std_] == ')':
            break
        if std_ == '^':
            RHS += '^'
            std_ += 1
            if expr[std_] == '-':
                RHS += '-'
                std_ += 1
            if expr[std_] == '(':
                rhs, std_ = get_exprs(expr,std_)
                RHS += rhs
                break
            if expr[std_].isalpha():
                RHS += expr[std_]
                break
            while std_ < len(expr) and  expr[std_].isnumeric():
                RHS += expr[std_]
                std_ += 1

        if expr[std_] in ('+','/','-','*'):
            if (RHS and expr[std_] in ('+','-')) or expr[std_] in ('*','/') :
                break
            
        RHS += expr[std_]
        std_ += 1
    if state:
       std = std_ 
    if not LHS:
        LHS = LSH = RHS
        RHS = None
    return LSH, LHS, RHS, std
