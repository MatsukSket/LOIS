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
  if abs(u - 1.0) < EPS:
    return v
  if abs(v - 1.0) < EPS:
    return u
  return 0.0


def weber_implication(a: float, b: float) -> float:
  if abs(a - 1.0) < EPS:
    return b
  return 1.0


def build_relation_matrix(
    A: FuzzySet, B: FuzzySet
) -> Dict[Tuple[str, str], float]:
  matrix = {}
  for x_elem, mu_a in A.elements.items():
    for y_elem, mu_b in B.elements.items():
      matrix[(x_elem, y_elem)] = weber_implication(mu_a, mu_b)
  return matrix


def fuzzy_compose(
    A_prime: FuzzySet,
    relation_matrix: Dict[Tuple[str, str], float],
    target_elements: List[str],
) -> Tuple[Dict[str, float], List[str]]:

  result = {}
  calc_details = []

  for y in target_elements:
    max_val = 0.0
    t_values = []
    for x, mu_a_prime in A_prime.elements.items():
      r_val = relation_matrix.get((x, y), 0.0)
      t_val = round(drastic_product(mu_a_prime, r_val), 4)
      t_values.append(t_val)
      if t_val > max_val:
        max_val = t_val

    res_val = round(max_val, 4)
    result[y] = res_val
    t_str = ', '.join(str(v) for v in t_values)
    calc_details.append(f'{y}: max({t_str}) = {res_val}')

  return result, calc_details


def are_fuzzy_sets_equal(s1: Dict[str, float], s2: Dict[str, float]) -> bool:
  if set(s1.keys()) != set(s2.keys()):
    return False
  return all(abs(s1[k] - s2[k]) < 1e-5 for k in s1)