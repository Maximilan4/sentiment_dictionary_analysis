ARITHMETIC = 'arithmetic'
GEOMETRIC_WEIGHTED = 'geometric'
HARMONIC_WEIGHTED = 'harmonic'


def arithmetic(values):
    """Среднее арифметическое"""
    if values:
        return sum(values) / float(len(values))
    else:
        return 0


def geometric_weighted(values):
    """Среднее геометрическое взвешенное"""
    weighted_sum = 0
    num = 1
    for el in values:
        weighted_sum += (el * (1 / float(2**num)))
        num += 1

    return weighted_sum


def harmonic_weighted(values):
    """Среднее гармоническое взвешенное"""
    weighted_sum = 0
    num = 2
    for el in values:
        weighted_sum += (el * (1 / float(num)))
        num += 1
    return weighted_sum
