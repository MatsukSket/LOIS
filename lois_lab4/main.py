"""Лабораторная работа №4 по ЛОИС, вариант 4. БГУИР, группа 421703.
Мацукевич Захар Александрович, Рассохов Егор Павлович, Полещук Ольга Владимировна.
Запуск программы и вывод множества значений посылки.
22.11.2026. Источник: условие лабораторной работы №4.
"""

from math import prod
from pathlib import Path

from fuzzy_operations import inverse_compose
from parser import read_problem


def format_value(value):
    denominator = value.denominator
    for factor in (2, 5):
        while denominator % factor == 0:
            denominator //= factor
    if denominator != 1:
        return str(value)
    integer, remainder = divmod(value.numerator, value.denominator)
    digits = []
    while remainder:
        digit, remainder = divmod(remainder * 10, value.denominator)
        digits.append(str(digit))
    return f"{integer}." + "".join(digits) if digits else str(integer)


def format_part(points):
    bounds = [(min(column), max(column)) for column in zip(*points)]
    corner_count = prod(len(set(pair)) for pair in bounds)
    if len(points) == corner_count and all(
        all(value in pair for value, pair in zip(point, bounds)) for point in points
    ):
        intervals = [f"[{format_value(low)};{format_value(high)}]" for low, high in bounds]
        return "(" + "×".join(intervals) + ")"

    # Выпуклая оболочка сохраняет связь между координатами.
    labels = ["<" + ",".join(map(format_value, point)) + ">" for point in points]
    return "conv{" + ",".join(labels) + "}"


def main():
    try:
        filename = input("Введите имя файла базы знаний [knowledge_base.txt]: ").strip()
        if not filename:
            filename = Path(__file__).with_name("knowledge_base.txt")
        predicate, orders = read_problem(filename)
        if len(orders) == 2:
            choice = input("Обе таблицы однострочные. Какая содержит правило (1/2)? ").strip()
            if choice not in ("1", "2"):
                raise ValueError("Введите номер таблицы 1 или 2.")
            rule, result = orders[int(choice) - 1]
        else:
            rule, result = orders[0]
        parts = inverse_compose(rule.rows, result.rows[0])
    except (OSError, ValueError, EOFError) as error:
        print(f"Ошибка ввода: {error}")
        return 1

    names = ",".join(f"{predicate}({name})" for name in rule.names)
    if parts:
        solution = "∪".join(map(format_part, parts))
        print(f"{solution} ∋ <{names}>")
    else:
        print(f"∅ ∌ <{names}>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
