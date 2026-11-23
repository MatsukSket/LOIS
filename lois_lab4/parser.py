"""Лабораторная работа №4 по ЛОИС, вариант 4. БГУИР, группа 421703.
Мацукевич Захар Александрович
Рассохов Егор Павлович
Полещук Ольга Владимировна.
Чтение таблиц правила и следствия.
22.11.2026. Источник: условие лабораторной работы №4.
"""

import re
from pathlib import Path


def read_table(block):
    lines = block.splitlines()
    names = lines[0].split()
    if not all(re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", name) for name in names):
        raise ValueError("Недопустимое имя элемента домена.")
    if len(set(names)) != len(names):
        raise ValueError("Имена внутри одного домена должны быть различны.")
    rows = []
    for line in lines[1:]:
        values = line.split()
        if len(values) != len(names):
            raise ValueError("Число значений в строке не совпадает с числом элементов.")
        if not all(re.fullmatch(r"(?:0(?:\.[0-9]+)?|1(?:\.0+)?)", v) for v in values):
            raise ValueError("Степени принадлежности задаются числами от 0 до 1.")
        rows.append([float(v) for v in values])
    if not rows:
        raise ValueError("В таблице отсутствуют значения.")
    return names, rows


def read_problem(path):
    content = Path(path).read_text(encoding="utf-8-sig").strip()
    blocks = re.split(r"\n[ \t]*\n(?:[ \t]*\n)*", content)
    if len(blocks) != 3 or not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", blocks[0]):
        raise ValueError("Нужны имя посылки и две таблицы, разделённые пустыми строками.")
    predicate, result_block, rule_block = blocks
    y_names, y_rows = read_table(result_block)
    if len(y_rows) != 1:
        raise ValueError("Таблица y должна содержать одну строку значений.")
    x_names, rule = read_table(rule_block)
    if len(rule) != len(y_names):
        raise ValueError("В таблице x должно быть по одной строке значений на каждый y.")
    return predicate, x_names, rule, y_rows[0]
