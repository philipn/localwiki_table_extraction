from urlparse import urljoin
import re

import slumber

from extract import get_data

IMPORT_SITE = 'http://127.0.0.1:8000'

api_endpoint = urljoin(IMPORT_SITE, 'api/')
api = slumber.API(api_endpoint)


MAX_ATTRIBUTE_LENGTH = 50


def format_attribute(name):
    name = name.strip().lower()

    # Change spaces to underscores
    name = '_'.join(name.split())

    if name[0] in '0123456789':
       # TODO XXX hack, need better solution
       # maybe remove the leading numbers?
        name = 's_%s' % name

    # Remove non alphanumeric characters
    attribute = re.sub('[^\w]', '', name)

    # TODO XXX do something better here
    return attribute[:MAX_ATTRIBUTE_LENGTH]


def format_value(unencoded_value, attribute_name, datatype):
    # TODO
    return unencoded_value


def guess_datatype(attribute_name, unencoded_value):
    # TODO
    return 'text'


def import_on(pagename, infos):
    for name, unencoded_value in infos.iteritems():
        # Check to see that attribute exists.
        attribute = format_attribute(name)

        datatype = guess_datatype(name, unencoded_value)
        value = format_value(unencoded_value, name, datatype)

        if not api.page_info_attribute.get(attribute=attribute)['objects']:
            api.page_info_attribute.post({
                'description': 'Add something here',
                'datatype': datatype,
                'name': name,
                'attribute': attribute,
                'required': False
            })

        # Check to make sure the datatype of the attribute is the same
        # as what we're adding.
        pass

        # Lookup page URI
        try:
            page_uri = api.page.get(name=pagename)['objects'][0]['resource_uri']
        except IndexError:
            # No page with that name, let's continue
            continue

        api.page_info.post({
            'page': page_uri,
            'attribute': attribute,
            'value': value
        })


for pagename, data in get_data().iteritems():
    import_on(pagename, data)
