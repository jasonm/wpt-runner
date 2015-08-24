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

# def save_test(server, label, test_id, status):
#     db.execute("insert into tests (server, label, test_id, status) values (%s, %s, %s, %s)", (server, label, test_id, status))

# TODO: naming: differentiate 'test_id' as psql tests table PK vs WPT test_id
def save_test_results(server, test_id):
    existing_id = None
    db.execute("select id from tests where test_id=%s;", (test_id,)) 
    rows = db.fetchall()
    if len(rows):
        existing_id = rows[0][0]

    results_json = json.loads(sh.webpagetest.results(test_id, server=server).stdout)
    har_json = json.loads(sh.webpagetest.har(test_id, server=server).stdout)
    video_json = json.loads(sh.webpagetest.video(test_id, server=server).stdout)
    html5_video_json = json.loads(sh.webpagetest.player(test_id, server=server).stdout)

db.execute("select id, server, label, test_id from tests where status = %s", (status.STARTED,))
for id, server, label, test_id in db.fetchall():
    print "Updating %s" % id

    result = sh.webpagetest.status(test_id, server=server)
    if result.exit_code != 0:
        logger.error("Error running webpagetest status command: %s" % result)
        continue

    output = json.loads(result.stdout)
    logger.info("Output of webpagetest status command: %s" % output)

    status_text = output['statusText']

    if status_text == 'Test Complete':
        db.execute("update tests set status = '%s' where id = %s" % (status.FINISHED, id))
        save_test_results(server, test_id)


# query = "SELECT * from runs;"
# db.execute(query)
# print "Existing runs:"
# for uuid, data in db.fetchall():
#     print uuid
#     print data
#     print


# runs
# 150820_7G_A52

# {
#   "statusCode": 200,
#   "statusText": "Ok",
#   "data": {
#     "testId": "150820_BC_9W8",
#     "ownerKey": "e20a765d4694dfd4ad7a2942428d828e1a18ba34",
#     "jsonUrl": "http://www.webpagetest.org/jsonResult.php?test=150820_BC_9W8",
#     "xmlUrl": "http://www.webpagetest.org/xmlResult/150820_BC_9W8/",
#     "userUrl": "http://www.webpagetest.org/result/150820_BC_9W8/",
#     "summaryCSV": "http://www.webpagetest.org/result/150820_BC_9W8/page_data.csv",
#     "detailCSV": "http://www.webpagetest.org/result/150820_BC_9W8/requests.csv"
#   }
# }

# 150820_8F_9PB "MKE Dulles Chrome Cable 2015-08-19T22:39:26.120389"
# Output:
# {
#   "statusCode": 200,
#   "statusText": "Ok",
#   "data": {
#     "testId": "150820_8F_9PB",
#     "ownerKey": "0cb4056d81c6a77841a7d5864b41e5a5b7db3043",
#     "jsonUrl": "http://www.webpagetest.org/jsonResult.php?test=150820_8F_9PB",
#     "xmlUrl": "http://www.webpagetest.org/xmlResult/150820_8F_9PB/",
#     "userUrl": "http://www.webpagetest.org/result/150820_8F_9PB/",
#     "summaryCSV": "http://www.webpagetest.org/result/150820_8F_9PB/page_data.csv",
#     "detailCSV": "http://www.webpagetest.org/result/150820_8F_9PB/requests.csv"
#   }
# }

# "statusText": "Test Complete"

