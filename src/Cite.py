from src import utils


class Cite:
    def __init__(self, authors, title, year, source, publisher, doi, cites, url, ptype):
        self.url = url
        self.cites = cites
        self.doi = doi
        self.publisher = publisher
        self.source = source
        self.year = year
        self.title = title
        self.authors = authors
        self.ptype = ptype
        self.cleansed = ""
        self.dict = None

    def __repr__(self):
        return self.authors

    def _dict(self):
        if self.dict:
            return self.dict
        self.dict = {
            'authors': self.authors,
            'title': self.title,
            'year': self.year,
            'source': self.source,
            'publisher': self.publisher,
            'doi': self.doi,
            'cites': self.cites,
            'url': self.url,
            'ptype': self.ptype
        }
        return self.dict

    def compare(self, other):
        self.clean()
        other.clean()
        return utils.ratio(self.cleansed, other.cleansed) > 0.8

    def clean(self):
        if self.cleansed != "":
            return self.cleansed
        self.cleansed = utils.clean(self.title)
        return self.cleansed
