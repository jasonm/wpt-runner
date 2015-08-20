import os
from dotenv import load_dotenv
import psycopg2
import urlparse
import sys
import logging

# dotenv
dotenv_path = os.path.join(os.path.dirname(os.path.realpath('__file__')), '.env')
load_dotenv(dotenv_path)

# logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

# database
urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.environ['DATABASE_URL'])
conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
conn.set_session(autocommit=True)
db = conn.cursor()
