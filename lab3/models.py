"""///////////////////////////////////////
Лабораторная работа 1 по дисциплине ЛОИС
Выполнена студентами группы 421703 БГУИР
Мацукевичем Захаром Александровичем
Рассоховым Егором Павловичем
Полещук Ольгой Владимировной
Модуль структур данных (модели нечетких множеств и правил)
Дата: 04.10.2026
///////////////////////////////////////"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class FuzzySet:
  """Представление нечеткого множества: имя и словарь {элемент: степень принадлежности}."""

  name: str
  elements: Dict[str, float]

  def __repr__(self) -> str:
    inner = ','.join(f'<{k},{v}>' for k, v in self.elements.items())
    return f'{self.name}={{{inner}}}'


@dataclass
class Rule:
  """Представление правила вида A(x)~>B(y)."""

  antecedent_pred: str
  antecedent_var: str
  consequent_pred: str
  consequent_var: str

  def __repr__(self) -> str:
    return f'{self.antecedent_pred}({self.antecedent_var})~>{self.consequent_pred}({self.consequent_var})'