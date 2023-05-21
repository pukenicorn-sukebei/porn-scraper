import unittest
from typing import List

from pydantic.dataclasses import dataclass

from app.services.scraper.regex import normalize_general_name


class ScraperRegexTest(unittest.TestCase):
    def test_normalize_general_name(self):
        @dataclass
        class TestCase:
            input: List[str]
            expected: str

        test_cases = [
            TestCase(expected='T28-602', input=['t28602', 't-28602', 't28-602']),
            TestCase(expected='STARS-087', input=['STARS087', 'STARS00087', 'STARS-087']),
            TestCase(expected='KAVR-087', input=['KAVR087', 'KAVR00087', 'KAVR-087']),
            TestCase(expected='TDMN-009', input=['TDMN009', 'TDMN00009', 'TDMN-009']),
            TestCase(expected='SSIS-513', input=['SSIS513', 'SSIS00513', 'SSIS-513']),
            TestCase(expected='DVDMS-868', input=['DVDMS868', 'DVDMS00868', 'DVDMS-868']),
            TestCase(expected='URVRSP-175', input=['URVRSP175', 'URVRSP00175', 'URVRSP-175']),
            TestCase(expected='MBDD-2076', input=['MBDD-2076', 'MBDD-2076', 'MBDD-2076']),
            TestCase(expected='KTRA-425e', input=['KTRA425e', 'KTRA00425e', 'KTRA-425e']),
            TestCase(expected='IBW-873z', input=['IBW873z', 'IBW00873z', 'IBW-873z']),
        ]

        for case in test_cases:
            for inp in case.input:
                actual = normalize_general_name(inp)
                self.assertEqual(
                    case.expected,
                    actual,
                    "Normalize General Name Failed; Expecting {}, Got {}".format(case.expected, actual)
                )
