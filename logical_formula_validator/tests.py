import pytest
import re

# Замените 'logical_formula' на имя вашего файла (без .py)
from logical_formula import LogicalFormula

# ==========================================
# 1. Тесты конструктора и пустых строк
# ==========================================

@pytest.mark.parametrize("empty_input", ["", "   ", None])
def test_empty_formula(empty_input):
    """Проверка выброса ошибки при пустой формуле."""
    with pytest.raises(ValueError, match="Ошибка: Формула пуста."):
        LogicalFormula(empty_input)

def test_internal_init():
    """Проверка внутреннего рекурсивного вызова (создается пустой объект)."""
    f = LogicalFormula(_is_internal=True)
    assert f.type is None
    assert f.val is None
    assert f.left is None
    assert f.right is None

def test_trailing_characters():
    """Проверка на наличие лишних символов после успешного разбора формулы."""
    with pytest.raises(ValueError, match=r"Синтаксическая ошибка: лишние символы '\)' в позиции 5\."):
        LogicalFormula("(A->B))")

# ==========================================
# 2. Тесты атомарных формул и переменных
# ==========================================

@pytest.mark.parametrize("valid_atomic", ["0", "1", "A", "Z", "X1", "Y99"])
def test_atomic_valid(valid_atomic):
    """Корректные атомарные формулы (константы и переменные с индексами)."""
    f = LogicalFormula(valid_atomic)
    assert f.type == 'atomic'
    assert str(f) == valid_atomic

@pytest.mark.parametrize("invalid_symbol", ["a", "2", "#", "+"])
def test_atomic_invalid_symbols(invalid_symbol):
    """Недопустимые символы в начале атомарной формулы."""
    # re.escape обезопасит спецсимволы (такие как +), чтобы regex не ломался
    expected_match = re.escape(f"Недопустимый символ '{invalid_symbol}'")
    with pytest.raises(ValueError, match=expected_match):
        LogicalFormula(invalid_symbol)

def test_variable_leading_zero():
    """Индекс переменной не должен начинаться с нуля."""
    with pytest.raises(ValueError, match=r"Индекс переменной не может начинаться с нуля \('01'\)"):
        LogicalFormula("A01")

def test_variable_out_of_bounds():
    """Индекс переменной не должен превышать 99."""
    with pytest.raises(ValueError, match=r"Индекс '100' вне допустимого диапазона"):
        LogicalFormula("Z100")

# ==========================================
# 3. Тесты обрывов строк (Unexpected EOF)
# ==========================================

def test_unexpected_eof_parse():
    """Обрыв строки прямо перед парсингом вложенного выражения."""
    with pytest.raises(ValueError, match="Ошибка парсинга в позиции 2: Неожиданный конец формулы."):
        LogicalFormula("(!") # Ожидается левый операнд, а строка кончилась

def test_unexpected_eof_compound():
    """Обрыв строки сразу после открывающей скобки."""
    with pytest.raises(ValueError, match=r"Неожиданный конец формулы после открывающей скобки '\('"):
        LogicalFormula("(")

def test_binary_eof_after_left():
    """Обрыв строки после парсинга левой части бинарной операции."""
    with pytest.raises(ValueError, match="Ожидался бинарный оператор после левого операнда."):
        LogicalFormula("(A")

# ==========================================
# 4. Тесты унарных и бинарных операций
# ==========================================

def test_unary_valid():
    """Корректная унарная операция."""
    f = LogicalFormula("(!A)")
    assert f.type == 'unary'
    assert str(f) == "(!A)"

def test_binary_invalid_operator():
    """Недопустимый бинарный оператор."""
    with pytest.raises(ValueError, match=r"Недопустимый бинарный оператор '\*'. Ожидался один из: &, \|, ->, ~, /\\, \\/."):
        LogicalFormula("(A*B)")

@pytest.mark.parametrize("formula_str", [
    "(A/\\B)",
    "(A\\/B)",
    "(A->B)",
    "(A~B)"
])
def test_binary_valid(formula_str):
    """Корректные бинарные операции всех доступных видов."""
    f = LogicalFormula(formula_str)
    assert f.type == 'binary'
    assert str(f) == formula_str

def test_complex_nested_formula():
    """Комплексный тест со вложенностью и игнорированием пробелов."""
    raw = "  ( ( ! A ) \\/ ( B5 -> ( C /\\ 0 ) ) )  "
    expected = "((!A)\\/(B5->(C/\\0)))"
    assert str(LogicalFormula(raw)) == expected

# ==========================================
# 5. Тесты проверки закрывающих скобок
# ==========================================

def test_expect_closing_bracket_eof():
    """Отсутствие скобки из-за конца строки."""
    with pytest.raises(ValueError, match=r"Ожидалась закрывающая скобка '\)' для унарной операции '!'. Получено: 'конец строки'"):
        LogicalFormula("(!A")

def test_expect_closing_bracket_actual_char():
    """Вместо закрывающей скобки стоит другой символ."""
    with pytest.raises(ValueError, match=r"Ожидалась закрывающая скобка '\)' для бинарной операции. Получено: '\+'"):
        LogicalFormula("(A/\\B+")