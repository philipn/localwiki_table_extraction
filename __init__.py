import slumber
from colors import rgb
import html5lib
import lxml.html
from collections import defaultdict
from lxml.html.clean import Cleaner
from lxml import etree
from urlparse import urljoin

from utils import all

SITE = "http://tasmania.localwiki.org/"

# We need some hints to figure out where the info table is
COLOR_HINT = rgb(232, 236, 239)

api_endpoint = urljoin(SITE, 'api/')

api = slumber.API(api_endpoint)


def strip_html(s):
    cleaner = Cleaner(style=True)
    html = lxml.html.fromstring(s)
    return cleaner.clean_html(html).text_content()


def extract_attrs_from_table(table):
    data = {}
    # Find a td with background-color the same as our COLOR_HINT.
    # This is our rough key.
    key = ''
    value = ''
    style = 'background-color: rgb(%s, %s, %s)' % (
            COLOR_HINT.red, COLOR_HINT.green, COLOR_HINT.blue)
    for td in table.findall('.//td'):
        if style in td.attrib.get('style', ''):
            if value:
                # We had a previous td with style set to COLOR_HINT
                # which means we should concatanate all of the
                # previous tds and make that the rough value associated
                # with the key.

                # Strip HTML from key.
                data[strip_html(key)] = value
                value = ''

            key = ''
            for elem in td.iterchildren():
                key += etree.tostring(elem)
        else:
            if td.text:
                value += td.text.strip()
            for elem in td.iterchildren():
                value += etree.tostring(elem)
            if td.tail:
                value += td.tail.strip()

    if value:
        data[strip_html(key)] = value

    return data


def extract_attributes(html):
    """
    @attr html: HTML, provided as a string.

    @returns: A dictionary of attribute -> value pairs, extracted from
              the table that's the likely "infobox" on the page.
    """
    # Heuristic: if the page has a table with its first row's
    # background color set to COLOR_HINT => we assume it's an info table.
    parser = html5lib.HTMLParser(
        tree=html5lib.treebuilders.getTreeBuilder("lxml"),
        namespaceHTMLElements=False)
    fragments = parser.parseFragment(html)
    root = etree.Element('div')
    for e in fragments:
        root.append(e)
    for table in root.findall('.//table'):
        first_td = table.find('.//td')
        style = 'background-color: rgb(%s, %s, %s)' % (
            COLOR_HINT.red, COLOR_HINT.green, COLOR_HINT.blue)
        if style in first_td.attrib.get('style', ''):
            # It's a match
            return extract_attrs_from_table(table)
    return {}


def normalize_key(key):
    return key


def normalize_value(value):
    return value


def get_data():
    page_data = defaultdict(dict)
    for page in all(api.page.get):
        pagename = page['name']
        print pagename
        for k, v in extract_attributes(page['content']).iteritems():
            page_data[pagename][normalize_key(k)] = normalize_value(v)
    return page_data


if __name__ == '__main__':
    print get_data()
