import re

from flask import jsonify

NOT_FOUND = "not_found"


def entry_in_first_week(line):
    """
    Takes a line of a log file and checks if the entry happened in the first 7 days of July 1995.

    :param line: The log file entry, eg '129.94.144.152 - - [01/Jul/1995:00:00:13 -0400] "GET / HTTP/1.0" 400 7074'
    :return: True | False
    """
    pattern = re.compile(r"^(\[0[1-7]/Jul/1995.*?)$")
    return bool(pattern.match(line))


def find_http_status_code(line):
    """
    Finds the HTTP status code in a log file entry. It's assumed that the code is printed after the request information
    containing the protocol, like 'HTTP/1.0"'.
    If a code is found it is returned, otherwise 'not_found' is returned.

    :param line: The log file entry, eg '129.94.144.152 - - [01/Jul/1995:00:00:13 -0400] "GET / HTTP/1.0" 400 7074'
    :return: status code, eg. 200 | not_found
    """
    arr = re.split(r".*?HTTP/.*\"\s", line)
    if len(arr) > 1:
        return arr[1][:3]
    return NOT_FOUND


class Result:
    """
    DTO for log file stats created with a LogParser. It contains the path to the log file, the number top 10
    requests per host/ip descending and the number of HTTP status codes 2xx, 3xx, 4xx, 5xx per day of the first
    7 days of Jul 1995.
    """
    def __init__(self, log_file_path, top_10_hosts, codes_first_week):
        self.log_file_path = log_file_path
        self.top_10_hosts = top_10_hosts
        self.codes_first_week = codes_first_week

    def get_as_json(self):
        return jsonify(
            log_file_path=self.log_file_path,
            top_10_hosts=self.top_10_hosts,
            codes_first_week=self.codes_first_week)
