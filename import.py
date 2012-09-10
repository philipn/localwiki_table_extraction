from urlparse import urljoin
import re

import slumber

from extract import get_data

IMPORT_SITE = 'http://127.0.0.1:8000'

api_endpoint = urljoin(IMPORT_SITE, 'api/')
api = slumber.API(api_endpoint)


def format_attribute(name):
     name = name.strip().lower()

     # Change spaces to underscores
     name = '_'.join(name.split())

     # Remove non alphanumeric characters
     return re.sub('[^\w]', '', name)


def format_value(value):
    return value


def import_on(pagename, infos):
    for name, unencoded_value in infos.iteritems():
        # Check to see that attribute exists.
        attribute = format_attribute(name)
        value = format_value(unencoded_value)
        if not api.page_info_attribute.get(attribute=attribute)['objects']:
            api.page_info_attribute.post({
                'description': 'Add something here',
                'datatype': 'text',
                'name': name,
                'attribute': attribute,
                'required': False
            })

        # Check to make sure the datatype of the attribute is the same
        # as what we're adding.
        pass

        # Lookup page URI
        page_uri = api.page.get(name=pagename)['objects'][0]['resource_uri']
        api.page_info.post({
            'page': page_uri,
            'attribute': attribute,
            'value': value
        })


for pagename, data in get_data().iteritems():
    import_on(pagename, data)
