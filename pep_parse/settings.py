import datetime as dt
from pathlib import Path

BOT_NAME = 'pep_parse'

SPIDER_MODULES = ['pep_parse.spiders']

ROBOTSTXT_OBEY = True

BASE_DIR = Path(__file__).parent.parent

FIELDS_NAME = ('Статус', 'Количество')
FILE_NAME = 'status_summary_{time}.csv'
DIR_OUTPUT = 'results'
DATE_FORMAT = '%Y-%m-%dT%H-%M-%S'
TIME_NOW = dt.datetime.now().strftime(DATE_FORMAT)

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}

FEEDS = {
    f'{DIR_OUTPUT}/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
        'overwrite': True
    }
}
