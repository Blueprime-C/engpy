def fragment_1(expr, var):
    retn = []
    for items in expr.struct:
        if var in str(items.power_list()):
            cf, va = items.__extract__
            for k, v in va.items():
                if var in str(v):
                    retn.append(k)

    return cf * retn[0], v if retn else None