import logging
from collections import namedtuple
from datetime import datetime, date
from typing import List

from echarts.LogParse import LogParse
from echarts.Sqlite3Template import Sqlite3Template

logging.basicConfig(filename='logs/echarts.log', level=logging.DEBUG)

Stats = namedtuple('Stats', 'id board_id crawl_rate response_success_count response_error_count '
                            'request_redirect_count page_load_timeout_count non_html_response_count '
                            'network_error_count filtered_duplicate_item_count filtered_item_count parse_error_count '
                            'parse_item_count date_time run_duration create_date_time data_type')


def insert(rows):
    db = Sqlite3Template('db/log.db')
    sql = """insert into stats(board_id,crawl_rate,response_success_count,response_error_count,
    request_redirect_count, page_load_timeout_count,non_html_response_count,network_error_count,
    filtered_duplicate_item_count, filtered_item_count,parse_error_count,parse_item_count,date_time,run_duration,
    create_date_time,data_type) values (?,?,?,?,?, ?,?,?,?,?,?,?,?,?,?,?) """

    for data in rows:
        d = datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')

        try:
            db.insert_data(sql, data['board_id'], data['crawlRate'], data['responseSuccessCount'],
                           data['responseErrorCount'], data['requestRedirectCount'], data['pageLoadTimeoutCount'],
                           data['nonHtmlResponseCount'], data['networkErrorCount'], data['filteredDuplicateItemCount'],
                           data['filteredItemCount'], data['parseErrorCount'], data['parseItemCount'], d,
                           data['run_duration'], datetime.now(), data['data_type'])
        except Exception as e:
            logging.info(e)

    db.close_db()


def fetch(data_type) -> List[Stats]:
    db = Sqlite3Template('db/log.db')
    today = datetime.now().replace(minute=0, hour=0, second=0, microsecond=0)

    rows = db.find_where('select * from stats where data_type = ? and date_time > ?', data_type, today)
    db.close_db()
    results = [Stats(*row) for row in rows]

    return results


def statis(rs: List[Stats]):
    tmp = {}
    for r in rs:
        for field in r._fields:
            if field.endswith('count'):
                tmp[field] = tmp.get(field, 0) + getattr(r, field, 0)
            else:
                tmp[field] = getattr(r, field)
    return Stats(**tmp)


if __name__ == '__main__':
    # Sqlite3Template('db/log.db').create_table('db/schema.sql')
    rows = LogParse('logs/flickr.log').data
    insert(rows)
