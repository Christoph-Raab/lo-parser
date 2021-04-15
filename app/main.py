import logging
import os
from flask import Flask, make_response, jsonify

from helpers import Result
from log_parser import LogParser

LISTEN_PORT = os.environ.get("LISTEN_PORT", 8080)
LOG_LEVEL = os.environ.get("LOG_LEVEL", logging.WARN)
LOG_FILE = os.environ.get("LOG_FILE", "../logs/NASA_access_log_Jul95")

app = Flask(__name__)
# Set JSON_SORT_KEYS to false to preserve descending order of hosts in the json response
app.config['JSON_SORT_KEYS'] = False
logging.getLogger().setLevel(LOG_LEVEL)


@app.route('/')
def get_log_file_stats():
    """
    Returns the stats for the configured log file as json, according to the LogParser on the base path '/'.
    If no stats for the log file were found a "Log file not found" message is returned. This might indicate that
    the log file could not be found. Please refer to app logs in that case.

    :return: json of the stats | Log not found message
    """
    res = LogParser.get_stats(LOG_FILE)
    if not isinstance(res, Result):
        logging.warning("File with path {} could not be parse!".format(LOG_FILE))
        return make_response(jsonify(message="Log file for path {} could not be parse!".format(LOG_FILE)), 400)
    return make_response(res.get_as_json(), 200)


with app.app_context():
    """
    After startup the logger will be initiated to parse the configured log file and cache the results.
    During this initial operation, the app can not yet process any requests.
    """
    logging.info("Initial parsing of log file with path {}, please wait...".format(LOG_FILE))
    try:
        LogParser.init(LOG_FILE)
    except ValueError as err:
        logging.error("Could not parse configured file!")
    logging.info("Done parsing! Ready to serve stats...")


if __name__ == "__main__":
    """Run flask app"""
    app.run(port=LISTEN_PORT)
    logging.info("Service running on port {}!".format(LISTEN_PORT))
