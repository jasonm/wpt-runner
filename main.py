#!/usr/bin/env python -Wignore
from dotenv import load_dotenv
from uuid import uuid1
import datetime
import os
import psycopg2
import urlparse
import sh
import json
import logging
import sys

# logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

# dotenv
dotenv_path = os.path.join(os.path.dirname(os.path.realpath('__file__')), '.env')
load_dotenv(dotenv_path)

# database
urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.environ['DATABASE_URL'])
conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
conn.set_session(autocommit=True)
db = conn.cursor()

common_options = {
  # Shared test options
  "key": os.getenv('WEBPAGETEST_API_KEY'),
  "video": True,
  "server": "http://www.webpagetest.org/"
}

test_configs = [
  {
    "label": "MKE Dulles MotoG 3G",
    "url": "https://www.minerva.kgi.edu",
    "options": {
      "location": "Dulles_MotoG",
      "connectivity": "3G",
    }
  },
  {
    "label": "MKE Dulles Chrome Cable",
    "url": "https://www.minerva.kgi.edu",
    "options": {
      "location": "Dulles",
      "connectivity": "Cable",
    }
  },
]

def maybe_quote(s):
    if isinstance(s, str) and " " in s:
        return "\"%s\"" % s
    else:
        return s

def save_test(server, label, test_id, status):
    db.execute("insert into tests (server, label, test_id, status) values (%s, %s, %s, %s)", (server, label, test_id, status))

for test_config in test_configs:
    run_label = "{} {}".format(test_config['label'], datetime.datetime.now().isoformat())
    options = {}
    options.update(common_options)
    options.update(test_config['options'])
    options.update({
        "label": run_label
    })

    options = {k: maybe_quote(v) for k,v in options.items()}

    logger.info("Running with options: %s" % options)

    result = sh.webpagetest.test(test_config['url'], **options)
    if result.exit_code != 0:
        logger.error("Error running webpagetest command: %s" % result)
        continue

    output = json.loads(result.stdout)
    logger.info("Output of webpagetest command: %s" % output)

    if output['statusCode'] != 200:
        logger.error("Error enqueuing webpagetest: %s" % output)
        continue

    save_test(server=options['server'], label=run_label, test_id=output['data']['testId'], status=output['statusText'])

    logger.info("Saved!")
