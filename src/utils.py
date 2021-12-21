import nltk
from difflib import SequenceMatcher
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import json
import requests


def str_equal(first, second):
    return ratio(first, second) >= 0.8


def ratio(first, second):
    return SequenceMatcher(None, first, second).ratio()


def find_first(item, _iter, _func):
    for index, i in enumerate(_iter):
        if _func(item, i):
            return i
    return None


def clean(text):
    text_tokens = word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
    res = " ".join(tokens_without_sw)
    res = re.sub(r'\W+', '', res)
    cleansed = res.lower()
    return cleansed


def scopus(title, api_key):
    try:
        url = "https://api.elsevier.com/content/search/scopus?apikey=[0]&query=TITLE%28%22[1]%22%29"
        query = url.replace('[0]', api_key).replace('[1]', title)
        page = requests.get(query)
        contents = page.content
        contents = json.loads(contents)
        entries = contents['search-results']['entry']
        for entry in entries:
            if 'dc:title' not in entry:
                return None

            dc:identifier
            eid
            dc:title
            prism:publicationName
            prism:isbn
            prism:coverDate
            prism:coverDisplayDate
            prism:doi
            citedby-count
            scopus_title = entry['dc:title']

            if ratio(scopus_title, title) > 0.8:
                return entry['link'][2]['@href']
        return None
    except Exception:
        return None


def get_scopus_url(title, api_key):
    try:
        url = "https://api.elsevier.com/content/search/scopus?apikey=[0]&query=TITLE%28%22[1]%22%29"
        query = url.replace('[0]', api_key).replace('[1]', title)
        page = requests.get(query)
        contents = page.content
        contents = json.loads(contents)
        entries = contents['search-results']['entry']
        for entry in entries:
            if 'dc:title' not in entry:
                return None
            scopus_title = entry['dc:title']
            if ratio(scopus_title, title) > 0.8:
                return entry['link'][2]['@href']
        return None
    except Exception:
        return None
