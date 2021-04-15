import unittest

from app.log_parser import LogParser
from app.main import app


class LogParserTestSuite(unittest.TestCase):
    def test_log_parser_works_with_cache(self):
        with app.app_context():
            # init
            log_file_path = "./app/tests/logfile"
            LogParser.init(log_file_path)

            # cache and data
            cache = LogParser.cache[log_file_path]
            self.assertTrue(cache)
            actual_log_file_path = cache.log_file_path
            res = LogParser.get_stats(log_file_path)

            self.assertEqual(log_file_path, actual_log_file_path)
            actual_top_10_hosts = cache.top_10_hosts
            expected_top_10_hosts = {
                "unicomp6.unicomp.net": 6, "burger.letters.com": 5, "199.120.110.21": 4,
                "d104.aa.net": 3, "129.94.144.152": 2, "199.72.81.55": 1
            }
            self.assertDictEqual(expected_top_10_hosts, actual_top_10_hosts)
            actual_codes_first_week = cache.codes_first_week
            expected_codes_first_week = {
                "01/Jul": {"2xx": 0, "3xx": 1, "4xx": 1, "5xx": 0},
                "02/Jul": {"2xx": 1, "3xx": 1, "4xx": 1, "5xx": 0},
                "03/Jul": {"2xx": 1, "3xx": 1, "4xx": 0, "5xx": 0},
                "04/Jul": {"2xx": 1, "3xx": 1, "4xx": 0, "5xx": 0},
                "05/Jul": {"2xx": 1, "3xx": 0, "4xx": 1, "5xx": 1},
                "06/Jul": {"2xx": 0, "3xx": 1, "4xx": 0, "5xx": 0},
                "07/Jul": {"2xx": 1, "3xx": 1, "4xx": 0, "5xx": 0}
            }
            self.assertDictEqual(expected_codes_first_week, actual_codes_first_week)

            # json response
            res_json = res.get_as_json()
            self.assertEqual(200, res_json.status_code)
            self.assertEqual("application/json", res_json.mimetype)

    def test_log_file_not_found_is_none(self):
        with app.app_context():
            res = LogParser.get_stats("./bad/file/path")
            self.assertIsNone(res)

