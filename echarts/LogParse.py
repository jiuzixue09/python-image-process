import os
import re
import json


class LogParse:

    def __init__(self, log_file: str):
        data = []
        with open(log_file, "r") as f:
            for line in f:
                if not line.strip():
                    continue  # skip the empty line
                m = re.search('crawl stats = (.+)', line)
                j = json.loads(m.group(1))
                time = re.search('([0-9]{4}-[0-9]{1,2}-[0-9]{1,2} [0-9]+:[0-9]+:[0-9]+)', line)
                j['time'] = time.group(1)
                board_id = re.search('board_id\\s*=\\s*([\\d]+)', line)
                j['board_id'] = int(board_id.group(1))
                j['data_type'] = log_file.split('/')[-1].split('.log')[0]
                data.append(j)

        self.data = data

    def stats(self):
        stats = {}
        for d in self.data:
            for key, value in d.items():
                if type(value) == str:
                    continue
                stats[key] = stats.get(key, 0) + value
        return stats

