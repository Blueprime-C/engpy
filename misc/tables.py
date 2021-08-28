from .assist import wrap, m_char


class D2_ord:
    def __init__(self, data, h_space=3, wdth=None, sep='', edge=True):
        self.data = data
        len_list = []
        _len_list = []
        for i in range(len(data[0])):
            for elements in data:
                len_list.append(len(str(elements[i])))
            _len_list.append(max(len_list))
            len_list = []
        self.h_space = h_space
        self.wdth = wdth
        self._len_list = _len_list
        self.sep = sep
        self.edge = edge

    def __str__(self):
        for i in range(len(self.data)):
            line = '[' if self.edge else '|' if self.edge is None else ''
            for c, j in enumerate(range(len(self.data[i]))):
                if c:
                    line += m_char(' ', self.h_space) + self.sep
                line += (wrap(self.data[i][j], self._len_list[j] if not self.wdth else self.wdth))
            line += ']' if self.edge else '|' if self.edge is None else ''
            print(line)
        return ''

    @property
    def cols(self):
        return len(self.data[0])
