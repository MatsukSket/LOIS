"""///////////////////////////////////////
Лабораторная работа 1 по дисциплине ЛОИС
Выполнена студентами группы 421703 БГУИР
Мацукевичем Захаром Александровичем
Рассоховым Егором Павловичем
Полещук Ольгой Владимировной
Модуль математических операций нечеткой логики (драстическая норма и импликация Вебера)
Дата: 04.10.2026
///////////////////////////////////////"""

from typing import Dict, List, Tuple
from models import FuzzySet

EPS = 1e-7


def drastic_product(u: float, v: float) -> float:
  """Треугольная норма драстического произведения TD(u, v)."""
  if abs(u - 1.0) < EPS:
    return v
  if abs(v - 1.0) < EPS:
    return u
  return 0.0


def weber_implication(a: float, b: float) -> float:
  """Нечеткая R-импликация Вебера IW(a, b)."""
  if abs(a - 1.0) < EPS:
    return b
  return 1.0


def build_relation_matrix(
    A: FuzzySet, B: FuzzySet
) -> Dict[Tuple[str, str], float]:
  """Построение матрицы бинарного отношения для правила A(x)~>B(y)."""
  matrix = {}
  for x_elem, mu_a in A.elements.items():
    for y_elem, mu_b in B.elements.items():
      matrix[(x_elem, y_elem)] = weber_implication(mu_a, mu_b)
  return matrix


def fuzzy_compose(
    A_prime: FuzzySet,
    relation_matrix: Dict[Tuple[str, str], float],
    target_elements: List[str],
) -> Dict[str, float]:
  """Композиционное правило вывода Заде: sup-TD (в дискретном случае max-TD)."""
  result = {}
  for y in target_elements:
    max_val = 0.0
    for x, mu_a_prime in A_prime.elements.items():
      r_val = relation_matrix.get((x, y), 0.0)
      t_val = drastic_product(mu_a_prime, r_val)
      if t_val > max_val:
        max_val = t_val
    result[y] = round(max_val, 4)
  return result


def are_fuzzy_sets_equal(s1: Dict[str, float], s2: Dict[str, float]) -> bool:
  """Проверка эквивалентности двух нечетких множеств с учетом погрешности float."""
  if set(s1.keys()) != set(s2.keys()):
    return False
  return all(abs(s1[k] - s2[k]) < 1e-5 for k in s1)