from bs4 import BeautifulSoup
from collections import OrderedDict
import requests
import csv
import json
import logging
import sys

logging.basicConfig(level=logging.INFO)

JSON_FILE = 'scraper.json'
CSV_FILE = 'export.csv'

overwriteCSV = True
pageCount = 0
sectionCount = 0


def init():
    data = readJSON()
    startScrapingPage(data, data['url'])


def startScrapingPage(data, url):
    logging.info('Scraping URL: %s' % url)
    soup = getPageContent(url)
    iterSections(soup, data)


def filterSoup(soup, data, filterByPos=False):
    # If filterByPos=False: returns a List of bs4 elements
    # If filterByPos=True: returns the filtered bs4 element
    try:
        content = soup.find_all(data['type'], class_=data['class'])
        if filterByPos:
            content = content[data['pos']]
        return content
    except IndexError:
        # print sys.exc_info()[0]
        logging.error("Something went wrong while filtering.")


def scrapeContent(soup, fields):
    global sectionCount
    content = OrderedDict()
    for key, value in fields.iteritems():
        try:
            content[key] = filterSoup(soup, value, True).get_text().strip()
        except AttributeError:
            content[key] = ''

    sectionCount += 1
    return content


def iterSections(soup, data):
    # If you want to scrape multiple sections
    # crete another json and run the program
    container = data['section']['container']
    fields = data['section']['content']

    sections = soup.find_all(container['type'], class_=container['class'])

    content = []
    for section in sections:
        content.append(scrapeContent(section, fields))

    export(content)

    findNext(soup, data)


def findNext(soup, data):
    try:
        container = data['next']['container']
        link = data['next']['link']
        nextPageLink = filterSoup(filterSoup(soup, container, True), link, True)
        if nextPageLink is None:
            logging.info('\n> All done! \n> Scraped %d section(s) in %d page(s)' % (sectionCount, pageCount))
        else:
            startScrapingPage(data, nextPageLink['href'])

    except KeyError:
        logging.error('Something went wrong while getting the next page')

    except IndexError:
        print sys.exc_info()[0]
        logging.error("Couldn't find the link to the next page. Please verify the 'next' values in the JSON")


def getPageContent(url):
    global pageCount
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    pageCount += 1
    return soup


def readJSON():
    with open(JSON_FILE) as data_file:
        data = json.load(data_file, object_pairs_hook=OrderedDict)

    return data


def export(data):
    global overwriteCSV
    if overwriteCSV:
        accessMethod = 'wb'
    else:
        accessMethod = 'ab'

    keys = data[0].keys()
    with open(CSV_FILE, accessMethod) as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        if overwriteCSV:
            dict_writer.writeheader()
        dict_writer.writerows(data)

    overwriteCSV = False


init()
