from typing import Optional, Union

from app.core.utils import (
    convert_string_to_float,
    convert_to_float_and_truncate,
)


class TestCoreUtils:
    """Тестирование утилит приложения core."""

    equal_test_data = (
        ('0', 0, 0, 'ноль'),
        ('-0', 0, 0, 'отрицательный ноль'),
        ('0.125', 0.125, 0, 'дробное число меньше 1'),
        ('0.125000', 0.125, 0, 'лишние нули дробной части'),
        ('-0.125', -0.125, 0, 'отрицательное дробное число меньше 1'),
        ('100', 100, 100, 'положительное целое число'),
        ('-100', -100, -100, 'отрицательное целое число'),
        ('000100', 100, 100, 'лишние нули целой части'),
        ('100.125', 100.125, 100, 'положительное дробное число'),
        ('-100.125', -100.125, -100, 'отрицательное дробное число'),
        ('000100.125000', 100.125, 100, 'лишние нули целой и дробной части'),
        ('', None, None, 'пустая строка'),
    )

    def message_creation(
        self,
        input_data: str,
        output_data: Optional[Union[int, float]],
        input_type: str,
    ) -> str:
        """Создание сообщения о тестировании.

        Args:
            input_data: входная строка.
            output_data: выходное число.
            input_type: строка с описанием входной строки.

        Returns:
            Преобразованное из строки число.
        """
        return (
            'Ошибка преобразования: '
            f'{input_type}. {input_data} к {output_data}'
        )

    def test_convert_string_to_float(self) -> None:
        """Тестирование преобразования строки во float."""
        for input_data, output_data, _, input_type in self.equal_test_data:
            assert (
                convert_string_to_float(input_data) == output_data
            ), self.message_creation(
                input_data,
                output_data,
                input_type,
            )

    def test_convert_string_to_float_and_truncate(self) -> None:
        """Тестирование преобразования строки во float."""
        for input_data, _, output_data, input_type in self.equal_test_data:
            assert (
                convert_to_float_and_truncate(input_data) == output_data
            ), self.message_creation(
                input_data,
                output_data,
                input_type,
            )
