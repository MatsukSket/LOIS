from logical_formula import LogicalFormula


def main():
    while True:
        try:
            user_input = input("\nВведите формулу: ")

            if user_input.strip().lower() in ['exit', 'quit']:
                print("Выход из программы. До свидания!")
                break

            if not user_input.strip():
                continue

            formula = LogicalFormula(user_input)

            print(f"Строка является формулой сокращенного языка логики высказываний")
            print(f"{formula}")

        except ValueError as e:
            print(f"ОШИБКА: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")


if __name__ == "__main__":
    main()