def _intable(num):
    try:
        return True if int(float(format(num).replace(' ',''))) == float(format(num).replace(' ','')) else False
    except Exception:
        return False


def _numable(num):
    if not intable(num):
        try:
            float(format(num).replace(' ', ''))
        except Exception:
            return False
    return True


def _alnumity(num):
    from .miscs import alnum
    al = alnum(num)
    return True if isinstance(alnum(num), (int, float)) else False


def intable_(num):
    try:
        return True if int(float(num)) == float(num) else False
    except Exception:
        return False


def numable(*num):
    
    return all([_numable(nums) for nums in num])


def intable(*num):
    
    return all([_intable(nums) for nums in num])


def alnumity(*num):
    return all([_alnumity(nums) for nums in num])


def counterable(num):
    return num.__str__().isalpha()

def roundnumable(nums):
    return True if round(float(nums), 10) == int(float(nums)) + 1 else False
