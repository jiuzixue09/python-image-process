import re
import json


class LogProcess:

    def __init__(self, log_file='logs/stats.log'):
        ds = []
        with open(log_file, "r") as f:
            for line in f:
                if not line.strip():
                    continue  # skip the empty line
                m = re.search('crawl stats = (.+)', line)
                j = json.loads(m.group(1))
                ds.append(j)

        stats = {}
        for d in ds:
            for key, value in d.items():
                if type(value) == str:
                    continue
                stats[key] = stats.get(key, 0) + value
        self.stats = stats
