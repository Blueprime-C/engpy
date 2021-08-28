from adem.misc.gen import getter

def _intable(num):
    try:
        return True if int(float(str(num.desolve if getter(num,
                                                           'desolve') else num).replace(' ',
                                                                                         ''))) == float(str(num.desolve if getter(num, 'desolve') else num).replace(' ','')) else False
    except Exception:
        return False
def _numable(num):
    if not intable(num):
        try:
            float(str(num.desolve if getter(num, 'desolve') else num).replace(' ',''))
        except Exception:
            return False
    return True

def intable_(num):
    try:
        return True if int(float(num.desolve if getter(num, 'desolve') else num)) == float(num.desolve if getter(num, 'desolve') else num) else False
    except Exception:
        return False

def numable(*num):
    
    return all([_numable(nums) for nums in num])

def intable(*num):
    
    return all([_intable(nums) for nums in num])



def counterable(num):
    return num.__str__().isalpha()
