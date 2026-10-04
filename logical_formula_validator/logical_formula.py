class LogicalFormula:
    def __init__(self, formula_str: str = None, _is_internal: bool = False):
        """
        Конструктор класса. Получает строку, инициирует парсинг и строит
        дерево формулы. _is_internal используется для рекурсивных вызовов.
        """
        self.type = None  # 'atomic', 'unary', 'binary'
        self.val = None
        self.left = None
        self.right = None

        if _is_internal:
            return

        if not formula_str or not formula_str.strip():
            raise ValueError("Ошибка: Формула пуста.")

        s = formula_str.replace(" ", "")
        s = s.replace("->", ">")
        s = s.replace("/\\", "&")
        s = s.replace("\\/", "|")

        idx = self._parse(s, 0)

        if idx != len(s):
            raise ValueError(f"Синтаксическая ошибка: лишние символы '{s[idx:]}' в позиции {idx}.")

    def _parse(self, s: str, idx: int) -> int:
        if idx >= len(s):
            raise ValueError(f"Ошибка парсинга в позиции {idx}: Неожиданный конец формулы.")

        if s[idx] == '(':
            return self._parse_compound(s, idx + 1)
        else:
            return self._parse_atomic(s, idx)

    def _parse_compound(self, s: str, idx: int) -> int:
        """Обрабатывает выражения внутри скобок."""
        if idx >= len(s):
            raise ValueError(
                f"Ошибка парсинга в позиции {idx}: Неожиданный конец формулы после открывающей скобки '('.")

        if s[idx] == '!':
            return self._parse_unary(s, idx)
        else:
            return self._parse_binary(s, idx)

    def _parse_unary(self, s: str, idx: int) -> int:
        """Парсит унарную операцию отрицания."""
        self.type = 'unary'
        self.val = '!'
        idx += 1

        self.left = LogicalFormula(_is_internal=True)
        idx = self.left._parse(s, idx)

        return self._expect_closing_bracket(s, idx, "унарной операции '!'")

    def _parse_binary(self, s: str, idx: int) -> int:
        """Парсит бинарные операции."""
        self.type = 'binary'

        self.left = LogicalFormula(_is_internal=True)
        idx = self.left._parse(s, idx)

        if idx >= len(s):
            raise ValueError(
                f"Ошибка парсинга в позиции {idx}: Неожиданный конец формулы. Ожидался бинарный оператор после левого операнда.")

        op = s[idx]
        if op not in ('&', '|', '>', '~'):
            raise ValueError(
                f"Ошибка парсинга в позиции {idx}: Недопустимый бинарный оператор '{op}'. Ожидался один из: &, |, ->, ~, /\\, \\/.")
        self.val = op
        idx += 1

        self.right = LogicalFormula(_is_internal=True)
        idx = self.right._parse(s, idx)

        return self._expect_closing_bracket(s, idx, "бинарной операции")

    def _parse_atomic(self, s: str, idx: int) -> int:
        """Обрабатывает атомарные формулы."""
        self.type = 'atomic'

        if s[idx] in ('1', '0'):
            self.val = s[idx]
            return idx + 1

        if s[idx] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            return self._parse_variable(s, idx)

        raise ValueError(
            f"Синтаксическая ошибка в позиции {idx}: Недопустимый символ '{s[idx]}'. Ожидалась переменная (A-Z), константа (0 или 1) или открывающая скобка '('.")

    def _parse_variable(self, s: str, idx: int) -> int:
        """Извлекает имя переменной."""
        start_idx = idx
        idx += 1
        num_str = ""

        while idx < len(s) and s[idx].isdigit():
            num_str += s[idx]
            idx += 1

        if num_str:
            if num_str.startswith('0'):
                raise ValueError(
                    f"Ошибка переменной в позиции {start_idx}: Индекс переменной не может начинаться с нуля ('{num_str}').")
            num = int(num_str)
            if not (1 <= num <= 99):
                raise ValueError(
                    f"Ошибка переменной в позиции {start_idx}: Индекс '{num}' вне допустимого диапазона (разрешено от 1 до 99).")

        self.val = s[start_idx:idx]
        return idx

    def _expect_closing_bracket(self, s: str, idx: int, context_msg: str) -> int:
        if idx >= len(s) or s[idx] != ')':
            actual_char = s[idx] if idx < len(s) else 'конец строки'
            raise ValueError(
                f"Ошибка парсинга в позиции {idx}: Ожидалась закрывающая скобка ')' для {context_msg}. Получено: '{actual_char}'.")
        return idx + 1

    def __str__(self) -> str:
        if self.type == 'atomic':
            return self.val
        elif self.type == 'unary':
            return f"(!{self.left})"
        elif self.type == 'binary':
            if self.val == '>':
                op = "->"
            elif self.val == '&':
                op = "/\\"
            elif self.val == '|':
                op = "\\/"
            else:
                op = self.val
            return f"({self.left}{op}{self.right})"