import os

from flask import Flask, render_template, request
from pyecharts.charts import Page

from echarts.ChartUtil import create_pie_chart, create_line_chart
from echarts.LogProcess import LogProcess

app = Flask(__name__)


@app.route('/statistics/<name>')
def statistics(name):
    html = "templates/{name}.html"

    if not os.path.exists(html):
        html_create(name)

    return render_template("{name}.html".format(name=name))


def html_create(name):
    html = "templates/{name}.html"

    lp = LogProcess('logs/{name}.log'.format(name=name))
    stats = lp.stats
    columns = ['responseSuccessCount',
               'responseErrorCount',
               'requestRedirectCount',
               'pageLoadTimeoutCount',
               'nonHtmlResponseCount',
               'networkErrorCount']
    data = [list((x, stats[x])) for x in columns]

    columns = ['filteredDuplicateItemCount',
               'parseErrorCount',
               'parseItemCount',
               ]

    data2 = [list((x, stats[x])) for x in columns]

    pie_chart = create_pie_chart(data, data2, title="统计图")

    raw = lp.raw

    xaxis = []
    yaxis_pair = []

    duplicate_item, parse_error, parse_item_count = [], [], []
    for r in raw:
        xaxis.append(r['time'])
        duplicate_item.append(r['filteredDuplicateItemCount'])
        parse_error.append(r['parseErrorCount'])
        parse_item_count.append(r['parseItemCount'])

    yaxis_pair.append(('filteredDuplicateItemCount', duplicate_item))
    yaxis_pair.append(('parseErrorCount', parse_error))
    yaxis_pair.append(('parseItemCount', parse_item_count))

    line_chart = create_line_chart(xaxis, yaxis_pair, title='时序图')

    page = Page(layout=Page.SimplePageLayout)
    page.add(
        pie_chart, line_chart
    )

    page.render(html.format(name=name))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
