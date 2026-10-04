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
  """Проверяет, совпадает ли полученный факт с уже существующим."""
  for name, fact in all_facts.items():
    if are_fuzzy_sets_equal(fact.elements, new_elements):
      return name
  return None


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

  # 1. Построение матриц нечетких отношений для каждого правила
  relation_matrices: Dict[Tuple[str, str], Dict[Tuple[str, str], float]] = {}
  for rule in rules:
    if rule.antecedent_pred not in facts or rule.consequent_pred not in facts:
      print(f'Предупреждение: для правила {rule} нет описания множеств в фактах.')
      continue

    matrix = build_relation_matrix(
        facts[rule.antecedent_pred], facts[rule.consequent_pred]
    )
    relation_matrices[(rule.antecedent_pred, rule.consequent_pred)] = matrix

  print('\n=== Начало прямого логического вывода ===\n')

  new_fact_counter = 1
  iteration = 1

  # 2. Итерационный процесс насыщения фактов
  while True:
    print(f'--- Итерация {iteration} ---')
    added_in_this_step = 0
    current_facts_list = list(facts.values())

    for fact in current_facts_list:
      for rule in rules:
        if (rule.antecedent_pred, rule.consequent_pred) not in relation_matrices:
          continue

        # Проверка совместимости носителя: факт должен иметь ту же размерность
        template_ant = facts[rule.antecedent_pred]
        if set(fact.elements.keys()) != set(template_ant.elements.keys()):
          continue

        target_y_elements = list(facts[rule.consequent_pred].elements.keys())
        matrix = relation_matrices[
            (rule.antecedent_pred, rule.consequent_pred)
        ]

        # Вычисление композиции
        inferred_elements = fuzzy_compose(fact, matrix, target_y_elements)
        matched_name = find_matching_fact_name(facts, inferred_elements)

        elements_str = ','.join(
            f'<{k},{v}>' for k, v in inferred_elements.items()
        )

        if matched_name is not None:
          # Факт совпал с уже известным
          print(f'{{{fact.name}, {rule}}} |- {{{elements_str}}}={matched_name}')
        else:
          # Сгенерирован абсолютно новый факт
          new_fact_name = f'_{new_fact_counter}'
          new_fact_counter += 1

          new_fact = FuzzySet(name=new_fact_name, elements=inferred_elements)
          facts[new_fact_name] = new_fact
          added_in_this_step += 1

          print(
              f'{{{fact.name}, {rule}}} |-'
              f' {new_fact_name}={{{elements_str}}} [НОВЫЙ]'
          )

    if added_in_this_step == 0:
      print(
          '\nВывод завершен: новых фактов не найдено (база знаний'
          ' стабилизировалась).'
      )
      break

    iteration += 1
    user_choice = input(
        '\nПродолжить вывод на следующей итерации? (y/n): '
    ).strip().lower()
    if user_choice == 'n':
      print('Вывод прерван пользователем.')
      break


if __name__ == '__main__':
  main()