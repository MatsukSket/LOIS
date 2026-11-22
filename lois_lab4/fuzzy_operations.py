"""Лабораторная работа №4 по ЛОИС, вариант 4. БГУИР, группа 421703.
Мацукевич Захар Александрович, Рассохов Егор Павлович, Полещук Ольга Владимировна.
Обратный вывод для ограниченной суммы конъюнкций Лукасевича.
22.11.2026. Источник: условие лабораторной работы №4.
"""

from fractions import Fraction
from itertools import combinations, product


def intersection(equations, dimension):
    """Единственная точка пересечения гиперплоскостей, метод Гаусса."""
    matrix = [list(coeffs) + [rhs] for coeffs, rhs in equations]
    pivot = 0
    for col in range(dimension):
        row = next((i for i in range(pivot, len(matrix)) if matrix[i][col]), None)
        if row is None:
            return None
        matrix[pivot], matrix[row] = matrix[row], matrix[pivot]
        divisor = matrix[pivot][col]
        base = [Fraction(v) / divisor for v in matrix[pivot]]
        matrix[pivot] = base
        for i, other in enumerate(matrix):
            if i != pivot and other[col]:
                factor = other[col]
                matrix[i] = [v - factor * b for v, b in zip(other, base)]
        pivot += 1
    if any(row[-1] for row in matrix[pivot:]):
        return None
    return tuple(row[-1] for row in matrix[:pivot])


def vertices(bounds, rule, target):
    n = len(bounds)
    equalities, limits = [], []
    for i, (low, high) in enumerate(bounds):
        unit = tuple(int(i == j) for j in range(n))
        limits.append((tuple(-v for v in unit), -low))
        limits.append((unit, high))

    for row, value in zip(rule, target):
        least = sum(max(0, low + r - 1) for (low, _), r in zip(bounds, row))
        most = sum(max(0, high + r - 1) for (_, high), r in zip(bounds, row))
        if not min(1, least) <= value <= min(1, most):
            return frozenset()
        # На выбранной ячейке каждое слагаемое либо ноль, либо p_i + r_i - 1.
        active = tuple(int(low >= 1 - r) for (low, _), r in zip(bounds, row))
        rhs = value + sum(1 - r for r, used in zip(row, active) if used)
        if value == 1:
            limits.append((tuple(-v for v in active), -rhs))
        else:
            equalities.append((active, rhs))

    # В вершине часть неравенств обращается в равенства. Для вырожденной
    # области перебор также находит концы отрезка или единственную точку.
    points = set()
    for count in range(max(0, n - len(equalities)), n + 1):
        for faces in combinations(limits, count):
            point = intersection(equalities + list(faces), n)
            if point is not None and all(
                sum(a * x for a, x in zip(coeffs, point)) <= rhs for coeffs, rhs in limits
            ):
                points.add(point)
        # Все вершины требуют одного и того же числа независимых
        # дополнительных граней: размерность минус ранг равенств.
        if points:
            break
    return frozenset(points)


def inverse_compose(rule, target):
    """Каждый элемент ответа — вершины одного выпуклого многогранника."""
    axes = []
    for column in zip(*rule):
        cuts = sorted({0, 1, *(1 - r for r in column)})
        axes.append(list(zip(cuts, cuts[1:])))
    parts = set()
    for bounds in product(*axes):
        points = vertices(bounds, rule, target)
        if points:
            parts.add(points)
    return sorted(sorted(part) for part in parts if not any(part < other for other in parts))
