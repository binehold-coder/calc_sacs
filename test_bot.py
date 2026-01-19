"""
Модульные тесты для калькулятора мешков
"""

import unittest
from bot import SacsCalculator


class TestSacsCalculator(unittest.TestCase):
    """Тесты для класса SacsCalculator"""
    
    def test_example_from_requirements(self):
        """Тест примера из требований: 11 линий + 8 мешков = 113"""
        result = SacsCalculator.calculate(11, 8)
        self.assertEqual(result, 113)
        # Проверим расчёт:
        # 11 линий: 6 нечётных (1,3,5,7,9,11) + 5 чётных (2,4,6,8,10)
        # (6 × 10) + (5 × 9) + 8 = 60 + 45 + 8 = 113
    
    def test_single_line_single_bag(self):
        """1 линия + 1 мешок"""
        result = SacsCalculator.calculate(1, 1)
        # 1 линия = 10 мешков + 1 = 11
        self.assertEqual(result, 11)
    
    def test_two_lines_one_bag(self):
        """2 линии + 1 мешок"""
        result = SacsCalculator.calculate(2, 1)
        # 1 нечётная (10) + 1 чётная (9) + 1 = 20
        self.assertEqual(result, 20)
    
    def test_max_lines_max_bags(self):
        """17 линий + 10 мешков (максимум)"""
        result = SacsCalculator.calculate(17, 10)
        # 9 нечётных + 8 чётных + 10
        # (9 × 10) + (8 × 9) + 10 = 90 + 72 + 10 = 172
        self.assertEqual(result, 172)
    
    def test_invalid_lines_too_high(self):
        """Проверка валидации: линии > 17"""
        result = SacsCalculator.calculate(18, 5)
        self.assertIsNone(result)
    
    def test_invalid_lines_too_low(self):
        """Проверка валидации: линии < 1"""
        result = SacsCalculator.calculate(0, 5)
        self.assertIsNone(result)
    
    def test_invalid_bags_too_high(self):
        """Проверка валидации: мешки > 10"""
        result = SacsCalculator.calculate(5, 11)
        self.assertIsNone(result)
    
    def test_invalid_bags_too_low(self):
        """Проверка валидации: мешки < 1"""
        result = SacsCalculator.calculate(5, 0)
        self.assertIsNone(result)
    
    def test_input_validation_lines(self):
        """Проверка валидации линий"""
        self.assertTrue(SacsCalculator.is_valid_lines("5"))
        self.assertTrue(SacsCalculator.is_valid_lines("1"))
        self.assertTrue(SacsCalculator.is_valid_lines("17"))
    
    def test_input_validation_lines_invalid(self):
        """Проверка валидации некорректных линий"""
        self.assertFalse(SacsCalculator.is_valid_lines("0"))
        self.assertFalse(SacsCalculator.is_valid_lines("18"))
        self.assertFalse(SacsCalculator.is_valid_lines("abc"))
    
    def test_input_validation_bags(self):
        """Проверка валидации мешков"""
        self.assertTrue(SacsCalculator.is_valid_bags("5"))
        self.assertTrue(SacsCalculator.is_valid_bags("1"))
        self.assertTrue(SacsCalculator.is_valid_bags("10"))
    
    def test_input_validation_bags_invalid(self):
        """Проверка валидации некорректных мешков"""
        self.assertFalse(SacsCalculator.is_valid_bags("0"))
        self.assertFalse(SacsCalculator.is_valid_bags("11"))
        self.assertFalse(SacsCalculator.is_valid_bags("abc"))


class TestSacsCalculatorDetailedLogic(unittest.TestCase):
    """Детальные тесты логики расчёта"""
    
    def test_4_lines_calculation(self):
        """4 линии: 2 нечётные (20) + 2 чётные (18) + 1 = 39"""
        result = SacsCalculator.calculate(4, 1)
        # 2 нечётные (1, 3): 2 × 10 = 20
        # 2 чётные (2, 4): 2 × 9 = 18
        # + 1 мешок = 39
        self.assertEqual(result, 39)
    
    def test_6_lines_calculation(self):
        """6 линий: 3 нечётные (30) + 3 чётные (27) + 1 = 58"""
        result = SacsCalculator.calculate(6, 1)
        # 3 нечётные (1, 3, 5): 3 × 10 = 30
        # 3 чётные (2, 4, 6): 3 × 9 = 27
        # + 1 мешок = 58
        self.assertEqual(result, 58)
    
    def test_with_additional_bags(self):
        """5 линий + 5 мешков"""
        result = SacsCalculator.calculate(5, 5)
        # 3 нечётные (10, 10, 10) = 30
        # 2 чётные (9, 9) = 18
        # + 5 мешков = 53
        self.assertEqual(result, 53)


if __name__ == '__main__':
    unittest.main()
