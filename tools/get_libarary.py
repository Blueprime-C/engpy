class Name:
    def __init__(self,name,lib):
        mm = f'{name}.{lib}' ; m= getattr(name,lib)
        self.name_ = super(m);self.lib = lib
    @property
    def identity(self, sub_b = False):
        if sub_b:
            return super.__hash__(sub_b) ==  super.__hash__(self.lib)
        return super.__hash__(self.lib) % 10000 - (2000* 450)

import engpy
print(Name(engpy,'tools.Fizzes').identity)
    
