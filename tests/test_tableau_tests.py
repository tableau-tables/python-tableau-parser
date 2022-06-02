import unittest
from mdx_tableau import tableau


class TestTableauTest(unittest.TestCase):

    def test_looks_like_table(self):
        block = "\n".join([
                    "| a | b | c |",
                    "| d | e | f |",
                    "| g | h | i |",
                ])
        self.assertTrue(tableau.test(block))

    def test_just_two_lines(self):
        block = "\n".join([
                    "| a | b | c |",
                    "| d | e | f |",
                ])
        self.assertTrue(tableau.test(block))

    def test_but_not_one_line(self):
        block = "\n".join([
                    "| a | b | c |",
                ])
        self.assertFalse(tableau.test(block))

    def test_missing_opening_bar(self):
        block = "\n".join([
                    "| a | b | c |",
                    "  d | e | f |",
                    "| g | h | i |",
                ])
        self.assertFalse(tableau.test(block))

    def test_missing_closeing_bar(self):
        block = "\n".join([
                    "| a | b | c  ",
                    "| d | e | f |",
                    "| g | h | i |",
                ])
        self.assertFalse(tableau.test(block))

if __name__ == '__main__':
    unittest.main()
