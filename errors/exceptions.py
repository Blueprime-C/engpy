class OrderError(Exception):
    pass


class DimensionError(Exception):
    pass


class IncompatibleOrder(Exception):
    pass


class InvalidOperation(Exception):
    pass


class OperationNotAllowed(Exception):
     pass


class OutOfRange(Exception):
    pass


class ImprobableError(Exception):
    pass


class UnacceptableToken(ValueError):
    pass


class QueryError(Exception):
    pass


class KindError(Exception):
    pass


class Vague(Exception):
    pass


class Void(Exception):
    pass


class InvalidAttribute(AttributeError):
    pass


class InconsistencyError(UnacceptableToken):
    pass


class ConcurrenceError(Exception):
    pass


class ActionDuplicationError(Exception):
    pass
