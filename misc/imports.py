from errors.exceptions import UnacceptableToken


def create(obj):
    try:
        obj.recreate
        return obj.recreate
    except AttributeError:
        raise UnacceptableToken
