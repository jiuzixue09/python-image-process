import re
import json


class LogProcess:

    def __init__(self, log_file='logs/unsplash.log'):
        ds = []
        with open(log_file, "r") as f:
            for line in f:
                if not line.strip():
                    continue  # skip the empty line
                m = re.search('crawl stats = (.+)', line)
                j = json.loads(m.group(1))
                time = re.search('[0-9]{4}-[0-9]{1,2}-[0-9]{1,2} ([0-9]+:[0-9]+:[0-9]+)', line)
                j['time'] = time.group(1)
                ds.append(j)

        self.raw = ds

        stats = {}
        for d in ds:
            for key, value in d.items():
                if type(value) == str:
                    continue
                stats[key] = stats.get(key, 0) + value
        self.stats = stats
