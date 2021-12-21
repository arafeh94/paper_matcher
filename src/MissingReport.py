import csv
import logging
import pickle
import tqdm
import utils
from src import FileLoader, Parsers
import os
from src.Scopus import Scopus, Paper


class MissingReport:
    STATE_START = 0
    STATE_LOAD = 1
    STATE_GENERATE = 2
    STATE_CLEAN = 3
    STATE_CSV = 4

    @staticmethod
    def instance(scholar_path, scopus_path, scopus_api_key):
        if os.path.exists('./cache.pkl'):
            instance = pickle.load(open('./cache.pkl', 'rb'))
        else:
            instance = MissingReport(scholar_path, scopus_path, scopus_api_key)
        return instance

    def __init__(self, scholar_path, scopus_path, scopus_api_key):
        self.scholar_path = scholar_path
        self.scopus_path = scopus_path
        self.scopus_api_key = scopus_api_key
        self.papers = []
        self.reports = []
        self.state = self.STATE_START
        self.scopus = Scopus(scopus_api_key)

    def cache(self, state):
        self.state = state
        file = open('./cache.pkl', 'wb')
        pickle.dump(self, file)

    def load(self):
        list_scholar = FileLoader.list_csv(self.scholar_path)
        list_scopus = FileLoader.list_csv(self.scopus_path)
        for scholar_paper in list_scholar:
            scopus_paper = utils.find_first(scholar_paper, list_scopus, utils.str_equal)
            if scopus_paper:
                self.papers.append({
                    'name': scholar_paper.replace('.csv', ''),
                    'scholar': self.scholar_path + '/' + scholar_paper,
                    'scopus': self.scopus_path + '/' + scopus_paper,
                })
        self.cache(self.STATE_LOAD)

    def generate(self):
        scholar_parser = Parsers.ScholarParser()
        scopus_parser = Parsers.ScopusParser()
        for paper in tqdm.tqdm(self.papers, 'generating missing report'):
            scholar_citations = FileLoader.load_csv(paper['scholar'], scholar_parser)
            scopus_citations = FileLoader.load_csv(paper['scopus'], scopus_parser)
            missing_report = {
                'title': paper['name'],
                'missing': []
            }
            for index, scholar_cite in enumerate(scholar_citations):
                found = list(filter(lambda scopus_cite: scholar_cite.compare(scopus_cite), scopus_citations))
                if len(found) == 0:
                    missing_report['missing'].append({
                        'title': scholar_cite.title,
                        'url': scholar_cite.url,
                        'year': scholar_cite.year,
                        'scholar_cite': scholar_cite,
                    })
            if len(missing_report['missing']) > 0:
                self.reports.append(missing_report)
        self.cache(self.STATE_GENERATE)

    def clean(self):
        for item in tqdm.tqdm(self.reports, 'cleaning'):
            new_missing = []
            scopus_paper = self.scopus.fetch(item['title'])
            item['scopus_paper'] = scopus_paper
            for index, missing_citation in enumerate(item['missing']):
                missing_scopus_paper = self.scopus.fetch(missing_citation['title'])
                if missing_scopus_paper and int(scopus_paper.year()) <= int(missing_scopus_paper.year()) + 3:
                    missing_citation['scopus_paper'] = missing_scopus_paper
                    new_missing.append(missing_citation)
            item['missing'] = new_missing
        self.cache(self.STATE_CLEAN)

    def to_csv(self):
        csv_report = []
        for paper in tqdm.tqdm(self.reports, 'csv dump'):
            scopus_paper: Paper = paper['scopus_paper']
            missing_papers = paper['missing']
            for missing_paper in missing_papers:
                missing_scopus_paper: Paper = missing_paper['scopus_paper']
                csv_report.append([
                    scopus_paper.title, scopus_paper.url,
                    missing_scopus_paper.title, missing_scopus_paper.url
                ])
        with open('./report.csv', 'w', encoding="utf-8", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerows(csv_report)
        self.cache(self.STATE_CSV)

    def execute(self):
        methods = [self.load, self.generate, self.clean, self.to_csv]
        execution = self.state
        while execution < self.STATE_CSV:
            method = methods[execution]
            logging.getLogger('missing_report').debug(f"executing: {method}")
            method()
            execution = self.state
