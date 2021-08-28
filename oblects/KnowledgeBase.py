from AI import Bank
from misc.assist import getter
from errors.exceptions import UnacceptableToken, Vague

class Article:
    def __addKnowledge__(self, items):
        if not isinstance(items, dict):
            raise UnacceptableToken(f'Knowledge should be passed in as dictionary')
        save = Bank()
        name = getter(self, 'name')
        if name and not save[name]:
            save[name] = {}
        if 'Knowledge' in save[name]:
            for item, value in items.items():
                if not item in save[name]['Knowledge']:
                    save[name]['Knowledge'].update({item:value})
        else:
            save[name]['Knowledge'] = items
        save.change_state

    def __removedKnowledge__(self, items):
        if not isinstance(items, dict):
            raise UnacceptableToken(f'Knowledge should be passed in as dictionary')
        save = Bank()
        name = getter(self, 'name')
        if name and not save[name]:
            raise ImprobableError
        if 'Knowledge' in save[name]:
            for item, value in items.items():
                if item in save[name]['Knowledge']:
                    save[name]['Knowledge'].pop(item)
                else:
                    raise InvalidOperation(f'{item} not present')
        else:
            save[name]['Knowledge'] = items
        save.change_state

    @property
    def __Knowledge__(self):
        save = Bank()
        name = getter(self, 'name')
        if name and save[name]:
            if 'Knowledge' in save[name]:
                return save[name]['Knowledge']
        else:
            return None

        
    @property
    def __sequence__(self):
        pass

    def __option__(self):
        pass

    
    def __limit__(self):
        conditions = {'plane1': [(('arctan(B/A'), '<>', '0', 'pi/2')]}

    def _s_(self):
        {'sin(A)'  : '2sin(A/2)cos(A/2)',
                'cos(A)'  : 'cos2(A/2) - sin2(A/2)',
                'tan(A)'  : '2tan(A/2)/(1 - tan2(A/2))',
         ('Asin(T) + Bcos(T)','plane1') : '(A^2 + B^2)^.5sin(T + arctan(B/A))'
                }
