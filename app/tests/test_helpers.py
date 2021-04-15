import unittest

from app.helpers import find_http_status_code, entry_in_first_week


class HelpersTestSuite(unittest.TestCase):
    def test_date_in_first_week(self):
        jul_1 = entry_in_first_week("[01/Jul/1995:00:00:11 -0400] \"GET /shuttle/missions/HTTP/1.0\" 200 4179")
        self.assertTrue(jul_1)
        jul_2 = entry_in_first_week("[02/Jul/1995:00:00:11 -0400] \"GET /shuttle/missions/HTTP/1.0\" 200 4179")
        self.assertTrue(jul_2)
        jul_3 = entry_in_first_week("[03/Jul/1995:00:00:11 -0400] \"GET /shuttle/missions/HTTP/1.0\" 200 4179")
        self.assertTrue(jul_3)
        jul_4 = entry_in_first_week("[04/Jul/1995:00:00:11 -0400] \"GET /shuttle/missions/HTTP/1.0\" 200 4179")
        self.assertTrue(jul_4)
        jul_5 = entry_in_first_week("[05/Jul/1995:00:00:11 -0400] \"GET /shuttle/missions/HTTP/1.0\" 200 4179")
        self.assertTrue(jul_5)
        jul_6 = entry_in_first_week("[06/Jul/1995:00:00:11 -0400] \"GET /shuttle/missions/HTTP/1.0\" 200 4179")
        self.assertTrue(jul_6)
        jul_7 = entry_in_first_week("[07/Jul/1995:00:00:11 -0400] \"GET /shuttle/missions/HTTP/1.0\" 200 4179")
        self.assertTrue(jul_7)
        jul_8 = entry_in_first_week("[08/Jul/1995:00:00:11 -0400] \"GET /shuttle/missions/HTTP/1.0\" 200 4179")
        self.assertFalse(jul_8)
        jul_15 = entry_in_first_week("[15/Jul/1995:00:00:11 -0400] \"GET /shuttle/missions/HTTP/1.0\" 200 4179")
        self.assertFalse(jul_15)
        jul_27 = entry_in_first_week("[27/Jul/1995:00:00:11 -0400] \"GET /shuttle/missions/HTTP/1.0\" 200 4179")
        self.assertFalse(jul_27)
        jul_31 = entry_in_first_week("[31/Jul/1995:00:00:11 -0400] \"GET /shuttle/missions/HTTP/1.0\" 200 4179")
        self.assertFalse(jul_31)

    def test_get_response_code(self):
        line = "[01/Jul/1995:00:00:11 -0400] \"GET /shuttle/missions/HTTP/1.0\" 200 4179"
        code_2xx = find_http_status_code(line)
        self.assertEqual("200", code_2xx)
        line = "[01/Jul/1995:00:00:11 -0400] \"GET /shuttle/missions/ HTTP/1.0\" 302 4179"
        code_3xx = find_http_status_code(line)
        self.assertEqual("302", code_3xx)
        line = "[01/Jul/1995:00:00:11 -0400] \"GET /shuttle/missions/ HTTP/1.0\" 404 4179"
        code_4xx = find_http_status_code(line)
        self.assertEqual("404", code_4xx)
        line = "[01/Jul/1995:00:00:11 -0400] \"GET /shuttle/missions/sts-73/ HTTP/1.0\" 503 4179"
        code_5xx = find_http_status_code(line)
        self.assertEqual("503", code_5xx)
        line = "[01/Jul/1995:00:00:11 -0400] \"GET /shuttle/missions/sts 503 4179"
        code_not_found = find_http_status_code(line)
        self.assertEqual("not_found", code_not_found)
