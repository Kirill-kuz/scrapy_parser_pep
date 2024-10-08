import csv
from collections import defaultdict

from pep_parse.settings import (BASE_DIR,
                                DIR_OUTPUT,
                                FIELDS_NAME,
                                FILE_NAME,
                                TIME_NOW)


class PepParsePipeline:
    def __init__(self):
        self.results = defaultdict(int)
        self.result_dir = BASE_DIR / DIR_OUTPUT
        if not self.result_dir.exists():
            self.result_dir.mkdir(parents=True, exist_ok=True)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        pep_status = item['status']
        self.results[pep_status] += 1
        return item

    def close_spider(self, spider):
        file_dir = self.result_dir / FILE_NAME.format(
            time=TIME_NOW)
        with open(file_dir, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            data = [FIELDS_NAME] + [
                [key, val] for key, val in self.results.items()] + [
                    ['Total', sum(self.results.values())]]
            writer.writerows(data)
