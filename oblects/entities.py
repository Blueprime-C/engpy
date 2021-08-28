class Inf:
    def __init__(self, sign='+'):
        self.type = 1 if sign == '+' else -1 if sign == '+-' else 0

    def __neg__(self):
        v = Inf()
        v.type = 0
        return v

    def __bool__(self):
        return bool(self.type)

    def __pos__(self):
        v = Inf()
        v.type = 1
        return v

    def __abs__(self):
        v = Inf()
        v.type = -1
        return v

    def __repr__(self):
        return chr(8734) if self.type > 0 else chr(177) + chr(8734) if self.type < 0 else f'-{chr(8734)}'

    @property
    def pos(self):
        return self.type >= 1

    @property
    def neg(self):
        return not self.type

    @property
    def pos_neg(self):
        return self.type < 0
