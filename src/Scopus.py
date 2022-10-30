import datetime
import json
import requests

from src import utils


class Paper:
    def __init__(self, id, title, publisher, date, url, doi, cite_count):
        self.id = id
        self.title = title
        self.publisher = publisher
        self.date = date
        self.url = url
        self.doi = doi
        self.cite_count = cite_count

    def year(self):
        return datetime.datetime.strptime(self.date, "%Y-%m-%d").year


class Scopus:

    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.elsevier.com/content/search/scopus?apikey=[0]&query=TITLE%28%22[1]%22%29"

    def fetch(self, title) -> Paper:
        try:
            query = self.url.replace('[0]', self.api_key).replace('[1]', title)
            page = requests.get(query)
            contents = page.content
            contents = json.loads(contents)
            entries = contents['search-results']['entry']
            for entry in entries:
                if 'dc:title' not in entry:
                    return None
                if utils.ratio(entry['dc:title'], title) < 0.8:
                    continue
                paper = Paper(
                    entry['eid'],
                    entry['dc:title'],
                    entry['prism:publicationName'],
                    entry['prism:coverDate'],
                    entry['link'][2]['@href'],
                    entry['prism:doi'],
                    entry['citedby-count'],
                )
                return paper
            return None
        except Exception:
            return None
