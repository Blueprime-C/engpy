        # for expr_ in self.struct:
        #     for coeff, var in expr_.expr.items():
        #         val_=[]; pw = 0; coeff_ = coeff; __prev = ''
        #         for var__ in var:
        #             coeff = coeff_
        #             val = {};count = 0;prev = ''
        #             for __var in var__:
        #                 if getter(__var, 'name'):
        #                     pw = var__[__var]
        #                     print('qqqqqqqqqqqqqqqqqqqqqq')
        #                     print(__var.lin_diff(),'j__j')
        #                     prev = prev if prev else  Expr({1: [val]});
        #                     __var_ = (__var** var__[__var]).lin_diff()
        #                     prev = prev * __var_ + (__var** var__[__var]) * prev.lin_diff(values)
        #
        #
        #                 elif __var == var_:
        #                     pw = var__[__var]
        #                     if not prev:
        #                         coeff *= pw
        #                         if var__[__var] - 1:
        #                             val[var_] = var__[__var] - 1
        #                     else:
        #                         __var_ = (__var** var__[__var]).lin_diff()
        #                         prev = prev * __var_ + (__var** var__[__var]) * prev.lin_diff(values)
        #                 else:
        #                     val[__var] = var__[__var]
        #             print('rrrrrrrrtwvrybrby',val,'pop',__var,'oj jo',var__)
        #             if prev:
        #                 prev *= 10
        #                 for _prev in prev.struct:
        #                     coeffin = list(_prev.expr)[0]
        #                     if coeffin in tmp:
        #                         tmp[coeffin].append(_prev.expr[coeffin][0])
        #                     else:
        #                         tmp[coeffin] = _prev.expr[coeffin]
        #                 __prev = 1
        #             else:
        #                 val_.append(val)
        #                 __prev = ''
        #         if __prev and pw *coeff:
        #             if pw * coeff in tmp:
        #                 tmp[pw* coeff].append(val_[0])
        #             else:
        #                 tmp[pw* coeff] = val_
        # print('eyeyyeyeye',tmp)
        # return Expr(tmp,True).simp()
