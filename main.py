# settings.py
import os
# from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.realpath('__file__')), '.env')
load_dotenv(dotenv_path)

print os.environ.get('DATABASE_URL')

# database
import psycopg2
import os
import urlparse

urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.environ['DATABASE_URL'])

conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
cur = conn.cursor()

query = "SELECT * from runs;"
print cur.execute(query)
for uuid, data in cur.fetchall():
    print uuid
    print data
    print


# shell
# import sh
# print(sh.ls("/"))
from sh import webpagetest
import sh
print(sh.head(sh.webpagetest.locations(), "-n 10"))
print "..."
