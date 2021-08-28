from .settings import _math
from .settings import eng
from .settings import Bank
from .helpers import get_key_word, score, guage
from misc.assist import match_curly, getter
from misc.utilities import rep_coeff
from misc.abilities import numable
from misc.vars import greeks, _alpha, chars
from errors.exceptions import *
from operator import itemgetter
from copy import deepcopy, copy

from abc import ABCMeta, abstractmethod

def _hash(string):
    result = 1
    for char in string:
        result *= chars.index(char) ** 2
        result *= 2
        result += 200000
    return result

class Memory:

    def __init__(self):
        self.slot1 = []
        self.slot2 = []
        self.slot3 = set()
        self.slot4 = {}

    def __add__(self,other):
        self.slot1.append(deepcopy(other))

    @property
    def trace(self):
        return self.slot1

    def __getitem__(self, slot):
        
        return eval(f'self.slot{slot}')

    
def check_Knowledge(cls):
    if not getter(cls, '__Knowledge__'):
        raise UnacceptableToken('This class is not certified for AI')
    store = Bank(); name =  getter(cls, 'name')
    if name and not store[name]:
        store[name] = {}
    if 'Knowledge_test' in store[name] and store[name]['Knowledge_test'] == _hash(str(cls.__Knowledge__)):
            return True

    print('Changes detected in the AI models, verifying all models are true.....')
            
    for pairs, values in cls.__Knowledge__.items():
        try:
            if not cls.recreate(pairs) | cls.recreate(values):
                raise InvalidAttribute(f'A wrong model detected: {pairs} != {values}')
            
        except (UnacceptableToken,OperationNotAllowed, ImprobableError) as e :
            raise InvalidAttribute(f'An error occured, check again: {pairs} != {values}')
        
    store[name]['Knowledge_test'] = _hash(str(cls.__Knowledge__))
    store.change_state


    

class Implementation(metaclass = ABCMeta):
    
    @abstractmethod
    def __sequence__(self):
        return

    def __options__(self):
        return NotImplemented

    def __apply__(self, rules, eobj, reduce = False):
        eobj = eobj.simp()
        for rule in rules:
            for laws, equiv in rule.items():
                As = {}; coefff = ''
                
                _laws = self.recreate(laws)
                laws = str(_laws.simp()).replace(' ','')
                _equiv = self.recreate(equiv)
                keywords = [get_key_word(str(laws_)) for laws_ in _laws]
                
                get_splited = list(eobj.split(keywords))
                if not get_splited[1]:
                    continue
                after_rep = []; after_rep_ = []; skip_law = False
                for count, laws in enumerate(_laws.struct, 1):
                    if skip_law:
                        break
                    if numable(laws):
                        if reduce:
                            if laws in eobj:
                                after_rep.append(-laws)
                        else:
                            after_rep.append(-laws)
                        matched = True
                        continue
                    
                    coeff_ = laws._coeff
                    if not coeff_ in (1,-1):
                        
                        laws = laws.recreate({1 : laws.expr[coeff_]})
                    laws = str(laws).replace(' ','')
                    rep_wait = []; self.__applied__ = False; matched = False
                    first_coeff = False
                    if isinstance(get_splited[1], int):
                        break
                    for exprs in get_splited[1].struct:
                        if matched:
                            rep_wait.append(exprs)
                            continue
                        cap_count, count_cap = 0, 0
                        n = 0; get_args = ''; a = ''; o = 0
                        coeff = '';exprs_ = str(exprs).replace(' ','')
                        pause = False; curr = ''
                        revert = copy(As); check = ''; pas = False
                        while n < len(laws) and o < len(exprs_):
                            if laws[n] not in exprs_[o:] and not laws[n] in _alpha:
                                As  = copy(revert)
                                rep_wait.append(exprs); pas = True
                                break
                            if laws[n] == exprs_[o]:
                                get_args += laws[n]; check += laws[n]
                            elif not get_args:
                                if len(_laws) > 1 and not coeff and not n and not o: 
                                    if laws[0] == '-' and exprs_[0] != '-'  or laws[0] != '-' and exprs_[0] == '-':
                                        break
                                if not coefff:
                                    curr = count
                                coeff += exprs_[o]
                                n -= 1
                            elif laws[n] in _alpha:
                                cap = laws[n];a = '';cap_count += 1
                                pause = False
                                nxt_char = laws[n +1] if n + 1 < len(laws) else ''
                                if o < len(exprs) and exprs_[o] =='.':
                                    break
                                while o < len(exprs_):
                                    if exprs_[o] == ')':
                                        if not a.count('(') > a.count(')'):
                                            if ')' not in (laws[n], nxt_char) and check in exprs_[o:]:
                                                
                                                a = ''; As  = copy(revert); pause = True; n = -1; o -= 1
                                                cap_count -= 1
                                                coeff += get_args; get_args = ''; n = -1; o -= 1; pause  = True
                                            break
                                    if not coefff:
                                        coefff = coeff; first_coeff = True
                                    if (coefff != coeff and len(_laws) > 1) or nxt_char == exprs_[o]:
                                        get_args = '';break
                                    a += exprs_[o]; get_args += exprs_[o]; o += 1
                                check = ''
                                if cap in As and a != As[cap]:
                                    break
                                else:
                                    if a:
                                        count_cap += 1
                                        As.update({cap: a});o -= 1
                                    
                            elif pause:
                                if get_args:
                                    if not get_args[0] in ('-', '+'):
                                        n = 0
                                    else:
                                        if laws[n-1] in ('-', '+'):
                                            coeff += exprs_[o]
                                            o += 1
                                            continue
                                
                                coeff += get_args + exprs_[o]
                                
                                get_args = ''; n -= 1
                            elif get_args in exprs_[o:] or (get_args and get_args[0] in ('-', '+') and get_args[1:] in exprs_[o:]):
                                a = ''; As  = copy(revert); pause = True; n -=1; o -= 1; cap_count -= 1
                            else:
                                break
                            
                            n += 1; o += 1
                        if skip_law:
                            break
                        if pas:
                            continue
                        coeff += exprs_[o:]
                        if first_coeff:
                            coefff = coeff; first_coeff = False
                        if n < len(laws) or cap_count > count_cap or not As or not get_args or coefff != coeff:
                            As  = copy(revert);rep_wait.append(exprs)
                        else:
                            matched = True
                            if len(_laws) == 1 or count == len(_laws):
                                after_rep.append((coeff if coeff else 1) *_equiv.cal(As) *  (1 if len(_laws) > 1 else 1/coeff_))
                                
                            
                    get_splited[1] = sum(rep_wait)
                    if not matched and len(_laws) > 1:
                        skip_law  = True
                    if skip_law:
                        break
                if not matched:
                    return eobj
                eobj = (get_splited[0] + sum(after_rep) + sum(rep_wait)).simp()
                self.__applied__ = True
        return eobj

                
                

    @property
    def trace(self):
        if getter(self, 'bank') is None:
            self.bank = [Memory()]
        return self.bank[0]
    
    def __rule_match__(self, laws = '', reduce  =  False):
        laws = self.__Knowledge__ if not laws else laws
        
        sequence = self.__sequence__
        options = self.__options__
        scores = []
        for laws, equiv in laws.items():
            #fwd = score(laws); bwd = score(equiv)
            if reduce:
                if reduce == 'expand':
                    if len(laws) > len(equiv):
                        equiv_, guage_ = score(equiv, format(self)), guage(equiv)
                        if equiv_ *2 > guage_:
                            scores.append((equiv_/guage_, {equiv:laws}))
                    elif len(laws) < len(equiv):
                        laws_, guage_ = score(laws, format(self)), guage(laws)
                        if laws_ *2 > guage(laws):
                            scores.append((laws_/guage_, {laws:equiv}))
                    continue
                if len(laws) < len(equiv):
                    equiv_, guage_ = score(equiv, format(self)), guage(equiv)
                    if equiv_ *2 > guage_:
                        scores.append((equiv_/guage_, {equiv:laws}))
                elif len(laws) > len(equiv):
                    laws_, guage_ = score(laws, format(self)), guage(laws)
                    if laws_ *2 > guage(laws):
                        scores.append((laws_/guage_, {laws:equiv}))
            else:
                equiv_, guage_ = score(equiv, format(self)), guage(equiv)
                if equiv_ *2 > guage_:
                    scores.append((equiv_/guage_, {equiv:laws}))
                laws_, guage_ = score(laws, format(self)), guage(laws)
                if laws_ *2 > guage(laws):
                    scores.append((laws_/guage_, {laws:equiv}))
        return sorted(scores, key = itemgetter(0), reverse = True)
            
        keywords = [get_key_word(str(laws_)) for laws_ in self.recreate(self.crule[0])]
        splitted_keywords = self.split(keywords)
        if splitted_keywords[1]:
            return True

        keywords = [get_key_word(str(laws_)) for laws_ in self.recreate(self.crule[1])]
        splitted_keywords = self.split(keywords)
        if splitted_keywords[1]:
            return False

        return None

    def __process__(self, reduce = False):
        predefined_keywords = ['cos','sin',
                               'tan','cosh',
                               'sinh','e','^'
                               ,'log','sec'
                               ,'cosec','cot'] + greeks
        As = {}
        laws = self.__Knowledge__
        
        sequence = self.__sequence__
        options = self.__options__; emp = 0
        if not 'law_track' in self.trace[4]:
            self.trace[4]['law_track'] = ['']
        for x,y in (sorted(self.__rule_match__(reduce = 'expand'),
                          key = lambda rules: len(list(rules[1].values())[0]), reverse = True) if reduce == 'broad expand' else self.__rule_match__(reduce = reduce)):
            self.__applied__ = False
            res = self.__apply__([y],self)
            if y == self.trace[4]['law_track'][-1]:# Avoid repition of laws 
                continue
            if self.__applied__:
                self.trace[4]['law_track'].append(y)
                yield res
            if 'continue' in self.trace[3]:
                continue
            while self.__applied__ and self.__rule_match__(y,reduce = reduce):
                self.__applied__ = False
                res = self.__apply__([y],self)
            
                if self.__applied__:
                    
                    yield res
            emp = 1
            
    def __call__(self, action = 'next', reduce = False, **options):
        '''
        AI Implementation can be rewrite Object in another form based on the laws given
            The AI takes mainly 2 arguments; action and reduce
            The AI work in three modes, which are triggered by reduce: reduce set to true will
            prompt the AI to look for ways to rewrite the Objects in a more concise, else the AI will
            just try to rewrite the Obj based on AI models in either direction; this the default mode.
            However, if expand is provided and not False the AI will try to expand the Obj.

            AI being a generator generates a new Obj to replace the Obj itself. each AI operations has a chain keeping track of itself, this is triggered by action
            action can be 'next', 'continue', 'reject'.
            when action = 'next', will prompt the AI to resume from its current state or initiate a state if not already
            when action = 'continue' will prompt the AI to restart the AI based on the current state
            when action = 'reject' will prompt the AI to restore the Obj to the previous state, and then continue
            when action = 'restore' will prompt the AI to restore the Obj to the previous state
            when action = 'recover' will prompt the AI to restore the Obj to the initial state destructively.


            A = 2sin2(2θ) + 2cos2(2θ)
            To rewrite this Expr in a concise form
            >>> A = Expr('2sin2(2theta) + 2cos2(2theta)')
            >>> A(reduce = True)
            >>> A
            2

            Note that anytime one of the models is applied, the AI pause, save the state, the action arg
            can be used to control these states.
            
            A = sin(2φ) + sec2(α^2 + β^2 - γ^2) + 3cos(2ω) + 6sin2(ω) - tan2(α^2 + β^2 - γ^2)
            To expand this
            >>> A(expand = True)
            >>> A
            sec2(α^2 + β^2 - γ^2) + 3cos(2ω) + 2sin(φ)cos(φ) + 6sin2(ω) - tan2(α^2 + β^2 - γ^2)

            Now the sin(2φ) was expanded, Now to continue expanding, we set action to next,
            however, by default action is set to 'next'. 
            >>> A()  # or A(action = 'next')
            >>> A
	    sec2(α^2 + β^2 - γ^2) + 3cos2(ω) + 3sin2(ω) + 2sin(φ)cos(φ) - tan2(α^2 + β^2 - γ^2)
            Now 3cos(2ω) was expanded
	    >>> A()
            3cos2(ω) + 3sin2(ω) + 2sin(φ)cos(φ) +  1 

            This is because sec2(α^2 + β^2 - γ^2) was expanded to 1 + tan2(α^2 + β^2 - γ^2), which
            was added to - tan2(α^2 + β^2 - γ^2) to sum to 1

            if there's need to switch another mode, action can be set to continue
            Let's assume we need to reduce this
            >>> A(action = 'continue', reduce = True)
            >>> A 
            2sin(φ)cos(φ) + 4
	    with action set to continue, the AI will try to reduce from its current state which was
	    3cos2(ω) + 3sin2(ω) + 2sin(φ)cos(φ) +  1 
            to continue with thr reduction
            >>> A()    # or A(action = 'next')
 	    sin(2φ) + 4

	    it should be noted that with the action set to next, the AI continue the reduction as oppose to its
            operation above when it was exapnding. This is because the 'next' option prompt the AI to resume its
            current mode, which is reduction this time around.



            Thus, the AI has now rewrite the ExprObj,
            sin(2φ) + sec2(α^2 + β^2 - γ^2) + 3cos(2ω) + 6sin2(ω) - tan2(α^2 + β^2 - γ^2) to
            sin(2φ) + 4

            Comparision can be made to confirm. let B be a copy of A
            >>> B = A.duplicate()
            Now we can use the recover action to recover the original expression of A
            >>> A('recover')
            >>> A
            sin(2φ) + sec2(α^2 + β^2 - γ^2) + 3cos(2ω) + 6sin2(ω) - tan2(α^2 + β^2 - γ^2)
            >>> A | B
            True

            Incase we wish to reject the expansion of sec2(α^2 + β^2 - γ^2) for sin(2φ), we use the
            reject action

            A = sin(2φ) + sec2(α^2 + β^2 - γ^2) + 3cos(2ω) + 6sin2(ω) - tan2(α^2 + β^2 - γ^2)
            To expand this
            >>> A(expand = True)
            >>> A()  # or A(action = 'next')
	    >>> A()
            >>> A
            3cos2(ω) + 3sin2(ω) + 2sin(φ)cos(φ) +  1
            >>> A(action = 'reject')
            >>> A
            sec2(α^2 + β^2 - γ^2) + 3cos2(ω) + 3sin2(ω) + 2sin(φ)cos( - φ) - tan2(α^2 + β^2 - γ^2)
            We can see that the expansion of sec2(α^2 + β^2 - γ^2) was reversed, and the operation resumed
            from the previous state when 3cos(2ω) was expanded

            >>> A('continue', reduce = True)
            >>> A()
	    >>>A
            sec2(α^2 + β^2 - γ^2) + 2sin(φ)cos(φ) - tan2(α^2 + β^2 - γ^2) + 3

            We can restore A to its previous state to continue expanding
            >>> A('restore')
            sec2(α^2 + β^2 - γ^2) + 3cos2(ω) + 3sin2(ω) + 2sin(φ)cos(φ) - tan2(α^2 + β^2 - γ^2)

            >>> A('continue', expand = True)
            >>> A
            3cos2(ω) + 3sin2(ω) + 2sin(φ)cos(φ) +  1

            >>> A('continue', reduce = True)
            >>> A
            2sin(φ)cos(φ) + 4
            
            To exapand, we can specified the degree; these are deep, broad expand, in_depth
            when expand =  deep, instead of the AI to pause states, it keep on expanding, till no
            none of the models can expand further.
            when expand = broad expand, the AI will rank all models available for expansion, the use the model
            with the highest rank to expand the Obj, and then pause the state.
            when expand = in_depth, the AI keep on working with exapand set 'to broad' expand till no further
            expansion is possible

            A = Expr('2sin(2φ) + 2sin(2ω)')
            >>> A(expand = 'deep')
            >>> A
            4sin(ω)cos( - ω) + 4sin(φ)cos(φ)
            
            We can see that all expansion was done before the AI pause

            A = 2sin(2φ) + 2sin(2ω)
            >>> A(expand = 'broad expand')
            >>> A
            4sin(φ + ω)cos(φ - ω)

            which can still be expanded further
            A = 2sin(2φ) + 2sin(2ω)
            >>> A(expand = 'in_depth')
            >>> A
            4sin(ω)cos2(φ)cos(ω) + 4sin2(ω)sin(φ)cos(φ) + 4sin(φ)cos2(ω)cos(φ) + 4sin2(φ)sin(ω)cos(ω)

            As AI is needed most time to reduce the Obj concisely, used the send method
            
            Z = tan2(α + βω) - 2xsin2(θ) + 2sin(δ)cos(δ) + 1 + 2xcos2(θ) 
            >>> z = Z.send()
            >>> z
            sec2(α + βω) + sin(2δ) + 2xcos(2θ)
            >>> Z 
            1  + tan2(α + βω) - 2xsin2(θ) + 2xcos2(θ) + 2sin(δ)cos(δ)
            
            meanwhile Z is still intact.

            However, if changes is to be make internally, set reduce = 'in_depth'
            Z = 1  + tan2(α + βω) - 2xsin2(θ) + 2xcos2(θ) + 2sin(δ)cos(δ)
            >>> Z(reduce = 'in_depth')
            >>> Z
            sec2(α + βω) + sin(2δ) + 2xcos(2θ)

            Now the change effected in Z itself
                    if getter(self, 'checked') is None:
            check_Knowledge(self)
            self.checked = True
        '''
        if 'expand' in options and options['expand']:
            if reduce:
                raise UnacceptableToken('reduce and expand options collision')
            elif options['expand'] == 'deep':
                self.__wrapper__(call = 'deep')
                return self.trace[1][-1]
            elif options['expand'] == 'in_depth':
                self.__wrapper__(call = 'deepest')
                return self.trace[1][-1]
            elif options['expand'] == 'broad expand':
                
                reduce = 'broad expand'
            elif options['expand'] == 'deepest':
                
                reduce = 'broad expand'
                
            else:
                reduce = 'expand'

        if reduce == 'in_depth':
            self.__wrapper__('r', call = 'deepest')
            return self.trace[1][-1]
            
        if not self.trace.trace:
            self.key = len(self.trace[2])
            self.trace[2].append(self.__process__(reduce))
            self.trace[4]['recv'] = self.duplicate()
            
        if action == 'restore':
            self.expr = self.trace[1][-1].expr
            return
        
        elif action == 'recover':
            self.expr = self.trace[4]['recv'].expr
            del self.bank
            return
        
        elif action == 'continue':
            self.key = len(self.trace[2])
            self.trace[2].append(self.__process__(reduce))
        elif action == 'reject':
            self.expr = self.trace[1][-1].expr
            self.trace[3].add('continue')
            del self.trace[1][-1]
        self.trace + self
        response = self.trace[2][-1]
        try:
            nxt_response = next(response)
        except StopIteration:
            nxt_response = self
        while options.get('expand') in ('all', 'deepest'):
            self.expr = nxt_response.expr
            self.trace + self
            try:
                nxt_response = next(response)
                
                
            except StopIteration:
                break
                    
        self.expr = nxt_response.expr


    def send(self):
        start = self.expr
        self(reduce = True)
        while self != self.trace[1][-1]:
            self(action = 'continue', reduce = True)
        self.expr = start
        to_return = self.trace[1][-1]
        del to_return.bank
        return  to_return

    def __wrapper__(self,mode = '', **kwargs):
        def deep(self, mode, degree = ''):
            start = self.duplicate()
            if not mode:
                self(expand = 'all' if not degree else degree)
            else:
                self(reduce = True)
            while len(self.trace[1]) < 2 or self.trace[1][-2] != self.trace[1][-1]:
                if not mode:
                    self(action = 'continue',expand = 'all' if not degree else degree)
                else:
                    self(action = 'continue', reduce = True)

        if 'call' in kwargs:
            if kwargs['call'] == 'deep':
                return deep(self, mode)
            elif kwargs['call'] == 'deepest':
                return deep(self,mode, 'deepest')
            
