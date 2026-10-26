"""///////////////////////////////////////
Лабораторная работа 1 по дисциплине ЛОИС
Выполнена студентами группы 421703 БГУИР
Мацукевичем Захаром Александровичем
Рассоховым Егором Павловичем
Полещук Ольгой Владимировной
Главный исполняемый модуль: прямой нечеткий вывод
Дата: 04.10.2026
///////////////////////////////////////"""

import os
from typing import Dict, List, Tuple
from fuzzy_operations import are_fuzzy_sets_equal, build_relation_matrix, fuzzy_compose
from models import FuzzySet, Rule
from parser import KnowledgeBaseParser


def find_matching_fact_name(
    all_facts: Dict[str, FuzzySet], new_elements: Dict[str, float]
) -> str | None:
  for name, fact in all_facts.items():
    if are_fuzzy_sets_equal(fact.elements, new_elements):
      return name
  return None


def print_relation_matrix(
    rule: Rule,
    A: FuzzySet,
    B: FuzzySet,
    matrix: Dict[Tuple[str, str], float],
) -> None:
  print(f'\nМатрица импликации Вебера для правила {rule}:')
  y_keys = list(B.elements.keys())
  header = 'x \\ y\t' + '\t'.join(f'{y}({B.elements[y]})' for y in y_keys)
  print(header)
  for x, mu_a in A.elements.items():
    row_vals = '\t'.join(f'{matrix[(x, y)]:.2f}' for y in y_keys)
    print(f'{x}({mu_a})\t{row_vals}')


def main():
  filename = input(
      'Введите имя файла базы знаний (по умолчанию knowledge_base.txt): '
  ).strip()
  if not filename:
    filename = 'knowledge_base.txt'

  if not os.path.exists(filename):
    print(f'Ошибка: файл {filename} не найден.')
    return

  facts, rules = KnowledgeBaseParser.parse_file(filename)
  print(f'\nУспешно загружено фактов: {len(facts)}, правил: {len(rules)}')
  print('Исходные факты:', ', '.join(str(f) for f in facts.values()))
  print('Правила:', ', '.join(str(r) for r in rules))

  # матрицы отношений для каждого правила
  relation_matrices: Dict[Tuple[str, str], Dict[Tuple[str, str], float]] = {}
  for rule in rules:
    if rule.antecedent_pred not in facts or rule.consequent_pred not in facts:
      print(
          f'Предупреждение: для правила {rule} нет описания множеств в фактах.'
      )
      continue

    ant_set = facts[rule.antecedent_pred]
    cons_set = facts[rule.consequent_pred]
    matrix = build_relation_matrix(ant_set, cons_set)
    relation_matrices[(rule.antecedent_pred, rule.consequent_pred)] = matrix
    print_relation_matrix(rule, ant_set, cons_set, matrix)

  print('\n=== Начало прямого логического вывода ===\n')

  new_fact_counter = 1
  iteration = 1

  # процесс насыщения фактов
  while True:
    print(f'--- Итерация {iteration} ---')
    added_in_this_step = 0
    current_facts_list = list(facts.values())

    for fact in current_facts_list:
      for rule in rules:
        if (
            rule.antecedent_pred,
            rule.consequent_pred,
        ) not in relation_matrices:
          continue

        # проверка совместимости носителя
        template_ant = facts[rule.antecedent_pred]
        if set(fact.elements.keys()) != set(template_ant.elements.keys()):
          continue

        target_y_elements = list(facts[rule.consequent_pred].elements.keys())
        matrix = relation_matrices[(rule.antecedent_pred, rule.consequent_pred)]

        # вычисление композиции с промежуточными деталями
        inferred_elements, calc_details = fuzzy_compose(
            fact, matrix, target_y_elements
        )
        matched_name = find_matching_fact_name(facts, inferred_elements)

        elements_str = ','.join(
            f'<{k},{v}>' for k, v in inferred_elements.items()
        )

        # печать промежуточного расчета
        print(f'  [Расчет для {{{fact.name}, {rule}}}]:')
        print('    ' + ' | '.join(calc_details))

        if matched_name is not None:
          print(
              f'  => {{{fact.name}, {rule}}} |- {{{elements_str}}}={matched_name}\n'
          )
        else:
          new_fact_name = f'_{new_fact_counter}'
          new_fact_counter += 1

          new_fact = FuzzySet(name=new_fact_name, elements=inferred_elements)
          facts[new_fact_name] = new_fact
          added_in_this_step += 1

          print(
              f'  => {{{fact.name}, {rule}}} |-'
              f' {new_fact_name}={{{elements_str}}} [НОВЫЙ]\n'
          )

    if added_in_this_step == 0:
      print(
          'Вывод завершен: новых фактов не найдено (база знаний'
          ' стабилизировалась).'
      )
      break

    iteration += 1
    user_choice = (
        input('Продолжить вывод на следующей итерации? (y/n): ')
        .strip()
        .lower()
    )
    if user_choice == 'n':
      print('Вывод прерван пользователем.')
      break


if __name__ == '__main__':
  main()