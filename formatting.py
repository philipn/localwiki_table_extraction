from urlparse import urljoin
import re
from utils import all

import slumber

from extract import get_data

SITE = 'http://127.0.0.1:8000'

api_endpoint = urljoin(SITE, 'api/')
api = slumber.API(api_endpoint)

from extract import find_info_table

def remove_info_tables():
    # TODO: use the info data to infer what pages to run this on
    for page in all(api.page.get):
        pagename = page['name']
    

remove_info_tables()
