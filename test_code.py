import unittest
from main import format_filename

class TestFormatAddress (unittest.TestCase):
    def test_format(self):
        filename = format_filename('Carrera 30 # 45 - 03')
        self.assertEqual(filename, "Carrera304503")

if __name__ == '__main__':
    unittest.main()