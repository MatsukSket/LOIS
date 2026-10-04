"""///////////////////////////////////////
Лабораторная работа 1 по дисциплине ЛОИС
Выполнена студентами группы 421703 БГУИР
Мацукевичем Захаром Александровичем
Рассоховым Егором Павловичем
Полещук Ольгой Владимировной
Модуль синтаксического анализа (парсер БНФ-грамматики базы знаний)
Дата: 04.10.2026
///////////////////////////////////////"""

import re
from typing import Dict, List, Tuple
from models import FuzzySet, Rule


class KnowledgeBaseParser:

  @staticmethod
  def clean_line(line: str) -> str:
    """Удаление пробелов и символов переноса строки."""
    return re.sub(r'\s+', '', line)

  @classmethod
  def parse_fuzzy_set(cls, line: str) -> FuzzySet:
    """Разбор строки факта вида: Name={<x1,0.0>,<x2,0.1>}"""
    line = cls.clean_line(line)
    match = re.match(r'^([A-Za-z0-9_]+)=\{([^}]+)\}$', line)
    if not match:
      raise ValueError(f'Некорректный синтаксис факта: {line}')

    name = match.group(1)
    pairs_str = match.group(2)

    elements: Dict[str, float] = {}
    pair_pattern = re.compile(r'<([A-Za-z0-9_]+),([0-9.]+)>')
    found_pairs = pair_pattern.findall(pairs_str)

    if not found_pairs:
      raise ValueError(f'Не найдены пары элементов в множестве: {line}')

    for elem, val in found_pairs:
      val_f = float(val)
      if not (0.0 <= val_f <= 1.0):
        raise ValueError(
            f'Степень принадлежности {val_f} выходит за границы [0, 1]'
        )
      elements[elem] = val_f

    return FuzzySet(name=name, elements=elements)

  @classmethod
  def parse_rule(cls, line: str) -> Rule:
    """Разбор строки правила вида: A(x)~>B(y)"""
    line = cls.clean_line(line)
    pattern = re.compile(
        r'^([A-Za-z0-9_]+)\(([A-Za-z0-9_]+)\)~>([A-Za-z0-9_]+)\(([A-Za-z0-9_]+)\)$'
    )
    match = pattern.match(line)
    if not match:
      raise ValueError(f'Некорректный синтаксис правила: {line}')

    return Rule(
        antecedent_pred=match.group(1),
        antecedent_var=match.group(2),
        consequent_pred=match.group(3),
        consequent_var=match.group(4),
    )

  @classmethod
  def parse_file(
      cls, filepath: str
  ) -> Tuple[Dict[str, FuzzySet], List[Rule]]:
    """Парсинг всего файла базы знаний."""
    facts: Dict[str, FuzzySet] = {}
    rules: List[Rule] = []

    with open(filepath, 'r', encoding='utf-8') as f:
      for line in f:
        clean = cls.clean_line(line)
        if not clean or clean.startswith('//'):
          continue
        if '~>' in clean:
          rules.append(cls.parse_rule(clean))
        elif '=' in clean and '{' in clean:
          fact = cls.parse_fuzzy_set(clean)
          facts[fact.name] = fact

    return facts, rules