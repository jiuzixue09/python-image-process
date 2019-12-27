import os

from flask import Flask, render_template, request
from pyecharts.charts import Page

from echarts.ChartUtil import create_pie_chart, create_line_chart, create_bar_chart
from echarts.LogParse import LogParse
from echarts.LogSqlService import fetch, statis

app = Flask(__name__)


@app.route('/statistics/<name>')
def statistics(name):
    html = "templates/{name}.html"

    if not os.path.exists(html):
        html_create(name)

    return render_template("{name}.html".format(name=name))


def html_create(name):
    html = "templates/{name}.html"

    rows = fetch(name)
    ss = statis(rows)

    data = [list(('response_success_count', ss.response_success_count)),
            list(('response_error_count', ss.response_error_count)),
            list(('request_redirect_count', ss.request_redirect_count)),
            list(('page_load_timeout_count', ss.page_load_timeout_count)),
            list(('non_html_response_count', ss.non_html_response_count)),
            list(('network_error_count', ss.network_error_count))]

    data2 = [list(('filtered_item_count', ss.filtered_item_count)),
             list(('filtered_duplicate_item_count', ss.filtered_duplicate_item_count)),
             list(('parse_item_count', ss.parse_item_count)), list(('parse_error_count', ss.parse_error_count))]

    pie_chart = create_pie_chart(data, data2, title="统计图")

    xaxis = []
    yaxis_pair = []

    duplicate_item, parse_error, parse_item_count,filtered_item_count = [], [], [], []
    for r in rows:
        xaxis.append(str(r.board_id))
        duplicate_item.append(r.filtered_duplicate_item_count)
        parse_error.append(r.parse_error_count)
        parse_item_count.append(r.parse_item_count)
        filtered_item_count.append(r.filtered_item_count)

    yaxis_pair.append(('filtered_duplicate_item_count', duplicate_item))
    yaxis_pair.append(('parse_error_count', parse_error))
    yaxis_pair.append(('parse_item_count', parse_item_count))
    yaxis_pair.append(('filtered_item_count', filtered_item_count))

    bar_chart = create_bar_chart(xaxis, yaxis_pair, title='board 统计图')

    xaxis, yaxis_pair = [], []
    crawl_rate, parse_rate = [], []

    index = -1
    for r in rows:
        t = str(r.date_time)[:-3]
        if t in xaxis:
            crawl_rate[index] += r.crawl_rate
            parse_rate[index] += (r.parse_item_count / (r.run_duration / 60))
        else:
            crawl_rate.append(r.crawl_rate)
            parse_rate.append(r.parse_item_count / (r.run_duration / 60))
            index += 1

        xaxis.append(t)
    crawl_rate = [round(x, 2) for x in crawl_rate]
    parse_rate = [round(x, 2) for x in parse_rate]
    yaxis_pair.append(('crawl_rate', crawl_rate))

    line_chart1 = create_line_chart(xaxis, yaxis_pair, title='每分钟请求量')

    yaxis_pair = [('parse_rate', parse_rate)]
    line_chart2 = create_line_chart(xaxis, yaxis_pair, title='每分钟解析量')

    page = Page(layout=Page.SimplePageLayout)
    page.add(
        pie_chart, bar_chart, line_chart1, line_chart2
    )

    page.render(html.format(name=name))


@app.route('/upload/<name>', methods=['GET', 'POST'])
def upload_file(name: str):
    if request.method == 'POST':
        f = request.files['file']
        f.save('logs/{name}.log'.format(name=name))
        return {"status": 1}
    return {"status": 0}


if __name__ == "__main__":
    app.run(host='0.0.0.0')
