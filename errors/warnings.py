from warnings import warn as warn_


def warn(message):
    warn_(message, DeprecationWarning, stacklevel=2)
