import json
import math
from path import base

try:
    with open(f'{base}/AI/engpy.config','r') as config:
        configuration = json.load(config)
except Exception:
    configuration = {}


def trig_index_simp():
    return configuration['math']['simp']['trig'][0]['index_simp']


class Math:
    def __new__(cls):
        if 'math' not in configuration:
            configuration['math'] = {}
        return super(Math,cls).__new__(cls)
    
    def __str__(self):
        return configuration['math'].__str__()
    
    @property
    def change_state(self):
        with open(f'{base}/AI/engpy.config','w+') as config:
            json.dump(configuration, config, indent = 4)
            
    def __add__(self,rule):
        configuration['math'].update(rule)
        self.change_state

    def __getitem__(self,other):
        return configuration['math'][other]


class Bank:
    def __init__(self):
        if 'bank' not in configuration:
            
            configuration['bank'] = {}
            self.change_state
    
    def __str__(self):
        return configuration['bank'].__str__()
    
    @property
    def change_state(self):
        with open(f'{base}/AI/engpy.config','w+') as config:
            json.dump(configuration, config, indent = 4)
            
    def __add__(self,rule):
        configuration['bank'].update(rule)
        self.change_state

    def remove(self,other):
        configuration['bank'].pop(other)
        self.change_state

    def __getitem__(self,other):
        return configuration['bank'][other] if other in configuration['bank'] else None

    def __setitem__(self,other, value):
        configuration['bank'][other] = value
        self.change_state


class Eng:
    def __new__(cls):
        if 'eng' not in configuration:
            configuration['eng'] = {}
        return super(Eng,cls).__new__(cls)
    def __str__(self):
        print('oul')
        return configuration['eng'].__str__()
    @property
    def change_state(self):
        with open(f'{base}/AI/engpy.config','w+') as config:
            json.dump(configuration, config, indent = 4)
            
    def __add__(self, rule):
        configuration['eng'].update(rule)
        self.change_state

    def __getitem__(self, other):
        return configuration['eng'][other]


_math = Math()
eng = Eng()
const = {'pi', math.pi}
if __name__ == "__main__":

    _math + {'working var':'x'}
    eng + {'working var':'t'}
