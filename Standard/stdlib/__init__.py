from ..internals import abs_


def abs(expr): return abs_(expr)


class Numbers:
    @staticmethod
    def plane_reflections(*numbers):
        for number in numbers:
            if not (number and -number in numbers):
                return False
        return True

    @staticmethod
    def reflected_planes(*numbers):
        return [number for number in numbers if number > 0 and -number in numbers]
