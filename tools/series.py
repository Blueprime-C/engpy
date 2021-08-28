from tools.exprs import Expr

class Series:

    def __new__(cls, expr,start = 0, stop = '', nth = 'n'):

        self = super(Series, cls).__new__(cls)

        self.expr =  Expr(expr)
        self.start = start
        self.stop = stop
        self.nth = nth
        return self

    def __str__(self):
        return self.expr.cal({self.nth : 'n'}).__str__() if self.nth != 'n' else str(self.expr)
    
    def __iter__(self):
        self.nxt = self.nextseq()
        return self
    
    def __next__(self):
        return next(self.nxt)

    def nextseq(self):
        for i in range(self.start, (self.stop if self.stop else 100)):
            yield self.expr.cal({self.nth: i})

    def cal(self,values):
        pass
    __repr__ = __str__

