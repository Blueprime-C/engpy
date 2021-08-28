from misc.assist import getter
from misc.miscs import alnum
from errors.exceptions import *
from misc.abilities import numable
from fundamentals.assorted import CD


def New_Raph(self,var):
    if getter(self, 'name') != 'Expr':
        raise UnacceptableToken(f'only Expr objects are allowed')
    starter = self.recreate('2'); int_ = 1
    derivative = self.lin_diff(var)
    if not derivative:
        raise ZeroDivisionError
    eval_ = derivative.cal({var: starter}, desolved=True)
    if eval_.iscomplex:
        raise OperationNotAllowed
    if not eval_:
        if self.cal({var: starter}) == 0:
            return starter
        else:
            eval_ += .2
    if abs(alnum(eval_)) < .1:
        starter = modified_New_Raph(self, var, starter)
        if starter.iscomplex:
            raise OperationNotAllowed
    count, grace, equals, prev_ = 0, 0, 0, self.recreate(0)
    while True:
        try:
            
            starter = starter.simp()
            if starter == prev_:
                equals += 1
            else: equals = 0
            prev_ = starter
            grad = self.cal({var: starter}, desolved=True) / derivative.cal({var: starter}, desolved=True)
            starter -= grad
            
            if not numable(grad):
                grad = grad.desolved
            if starter.iscomplex:
                raise OperationNotAllowed
            if not round(grad, 16):
                break
        except ZeroDivisionError:
            if self.cal({var: starter}) == 0:
                return starter.simp()
            starter += .5
        except InvalidOperation:
            raise ImprobableError
        if count > 15:
            if (grad > 0 and grad > prev) or (grad < 0 and grad < prev):
                if grace > 5:
                    
                    if not round(self.cal({var: starter}), 10):
                        return starter.simp()
                    raise ImprobableError
                grace += 1
        if equals == 6:
            if not round(self.cal({var: starter}), 10):
                return starter.simp()
            else:
                raise ImprobableError
        try:
            prev = grad
        except UnboundLocalError:
            pass
        count += 1
    return starter.simp()


def modified_New_Raph(self, var, value):
    if getter(self, 'name') != 'Expr':
        raise UnacceptableToken(f'only Expr objects are allowed')
    derivative = self.lin_diff(var)
    incr = derivative.lin_diff(var, 1, {var: value}, desolved=True)
    fx = self.cal({var: value})
    approx = alnum((-2 * fx/incr) ** .5)
    return value + approx if alnum(derivative.cal({var: value}, desolved=True)) * alnum(fx) < 0 else value - approx
