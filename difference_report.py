import codecs
import csv
import logging
import tqdm
from difflib import SequenceMatcher

from src.utils import clean

scopus_report_path = './sample/scopus.csv'
scholar_report_path = './sample/scholar.csv'


class IntCite:
    def __init__(self, cites, auths, title, publisher, year, url):
        self.title = title
        self.cites = cites
        self.auths = auths
        self.year = year
        self.publisher = publisher
        self.url = url
        self.clean = None

    def cleansed(self):
        self.clean = self.clean or clean(self.title)
        return self.clean

    def compare(self, other: 'IntCite'):
        return SequenceMatcher(None, self.cleansed(), other.cleansed()).ratio() > 0.8

    def __str__(self):
        return self.title + "," + self.cites


def load_file(file_name):
    results = []
    with codecs.open(file_name, encoding='iso-8859-1') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for index, row in enumerate(reader):
            acite = IntCite(row[0], row[1], row[2], row[3], row[4], row[5])
            results.append(acite)
    return results


logging.getLogger('main').debug("loading scopus")
scopus = load_file(scopus_report_path)
logging.getLogger('main').debug("loading scholar")
scholar = load_file(scholar_report_path)

dif_cites = [['title', 'scopus_cites', 'scholar_cites', 'auths', 'year', 'pub', 'url']]
for scholar_cite in tqdm.tqdm(scholar, 'generating report'):
    for scopus_cite in scopus:
        if scholar_cite.compare(scopus_cite):
            if scholar_cite.cites.isnumeric() and scopus_cite.cites.isnumeric():
                if int(scholar_cite.cites) != int(scopus_cite.cites):
                    values = list(scopus_cite.__dict__.values())
                    values.insert(2, scholar_cite.cites)
                    del values[-1]
                    dif_cites.append(values)

logging.getLogger('main').debug("writing csv")
with open('./difference_report.csv', 'w', encoding="utf-8", newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerows(dif_cites)
logging.getLogger('main').debug("writing done on file difference_report.csv")
