import itertools
import operator
import os
import logging

from helpers import entry_in_first_week, find_http_status_code, NOT_FOUND, Result


class LogParser:
    """
    LogParser takes a path to a log file and determines:

    1) The top 10 host/ip that requested the site in descending order.

    2) The number of HTTP status codes 2xx, 3xx, 4xx, 5xx per day.
    Currently this feature is only supported for the first 7 days of July 1995.

    The log parser can be initialized for a certain log file using the init() method.
    The stats for a log file are cached for future calls.
    """
    cache = {}

    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.requests_per_host = {}
        self.res_codes_first_week = {}

    @staticmethod
    def init(log_file_path):
        """
        Parses a given log file and caches the results for future calls.

        :param log_file_path: path to the log file
        :return: stats for the log file | None
        """
        if not os.access(log_file_path, os.R_OK):
            raise ValueError("File {} not found!".format(log_file_path))
        log_parser = LogParser(log_file_path)
        res = log_parser.run()
        LogParser.cache[log_file_path] = res
        return res

    @staticmethod
    def get_stats(log_file_path):
        """
        Returns the stats for a log file from the cache. If the cache does not contain it, the log file is parsed.

        :param log_file_path: path to the log file
        :return: stats for the log file (from cache)
        """
        if len(LogParser.cache) > 0 and log_file_path in LogParser.cache:
            logging.info("Serving stats for {} from cache".format(log_file_path))
            return LogParser.cache[log_file_path]
        logging.info("Stats for {} not in cache, parsing file...".format(log_file_path))
        try:
            return LogParser.init(log_file_path)
        except ValueError as err:
            logging.error(err)
            return None

    def run(self):
        """
        Parses the file and returns a Result of the found stats.

        :return: Result of the found stats
        """
        self.parse_file()
        top_10_requests_per_host = self.fetch_top_10_requests_per_host()
        return Result(self.log_file_path, top_10_requests_per_host, self.res_codes_first_week)

    def parse_file(self):
        """
        Reads the configured log file line by line. For each line the number of requests per host and the status codes
        are counted. It is assumed that the delimiter for host/ip and request/response information is ' - - '.

        A log file entry might contain invalid start bytes which should be ignored. Therefore errors is set to 'ignore'.
        """
        with open(self.log_file_path, "r", encoding="utf8", errors="ignore") as log_file:
            for line in log_file:
                arr = line.split(" - - ")
                if len(arr) > 1:
                    self.count_requests_per_hosts(arr[0])
                    self.count_status_codes(arr[1])

    def count_requests_per_hosts(self, host):
        """
        Counts the requests per host/ip

        :param host: the host/ip, eg. unicomp6.unicomp.net or 129.94.144.152
        """
        if host not in self.requests_per_host:
            self.requests_per_host[host] = 0
        self.requests_per_host[host] += 1

    def count_status_codes(self, line):
        """
        Checks if the log file entry is from the first 7 days of July 1995. If so the response code is extracted and
        added to the stats for the day of the entry. If no response code is found, the entry is ignored.

        :param line: a log file entry part, eg '[01/Jul/1995:00:00:11 -0400] \"GET / HTTP/1.0\" 200 4179'
        """
        if entry_in_first_week(line):
            date = line[1:7]
            if date not in self.res_codes_first_week:
                self.res_codes_first_week[date] = {"2xx": 0, "3xx": 0, "4xx": 0, "5xx": 0}
            code = find_http_status_code(line)
            if code != NOT_FOUND:
                entry = code[:1] + "xx"
                self.res_codes_first_week[date][entry] += 1

    def fetch_top_10_requests_per_host(self):
        """
        Converts the list of requests per host/ip into a descending sorted list and returns the top 10 of that list.

        :return: top 10 of number of requests per host/ip
        """
        top_10 = dict(sorted(self.requests_per_host.items(), key=operator.itemgetter(1), reverse=True))
        return dict(itertools.islice(top_10.items(), 0, 10))
