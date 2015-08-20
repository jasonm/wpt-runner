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

db.execute("select id, server, label, test_id from tests where status = %s", (status.STARTED,))

for id, server, label, test_id in db.fetchall():
    print "Updating %s" % id

    result = sh.webpagetest.status(test_id)
    if result.exit_code != 0:
        logger.error("Error running webpagetest status command: %s" % result)
        continue

    output = json.loads(result.stdout)
    logger.info("Output of webpagetest status command: %s" % output)

    status_text = output['statusText']

    if status_text == 'Test Complete':
        db.execute("update tests set status = '%s' where id = %s" % (status.FINISHED, id))
