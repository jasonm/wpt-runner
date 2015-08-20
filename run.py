#!/usr/bin/env python -Wignore
from uuid import uuid1
import datetime
import os
import sh
import json

import status
import commons

logger = commons.logger
db = commons.db

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

    save_test(server=options['server'], label=run_label, test_id=output['data']['testId'], status=status.STARTED)

    logger.info("Saved!")
