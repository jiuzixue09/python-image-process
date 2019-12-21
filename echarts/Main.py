from flask import Flask, render_template, request
from pyecharts.charts import Page

from echarts.ChartUtil import create_pie_chart, line_base
from echarts.LogProcess import LogProcess

app = Flask(__name__)


@app.route('/test')
def test():
    columns = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    data = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
    x = [list(z) for z in zip(columns, data)]

    columns = ["May", "Jun", "Jul", "Aug", "Sep", "Oct", "Bb", "Aa"]
    data = [25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
    x2 = [list(z) for z in zip(columns, data)]

    pie_chart = create_pie_chart(x,x2, title="基本示例")
    line_chart = line_base()

    page = Page(layout=Page.SimplePageLayout)
    page.add(
        pie_chart, line_chart
    )
    page.render("templates/index.html")
    return render_template("index.html")


@app.route('/statistics/req/<name>')
def req(name):
    lp = LogProcess()
    stats = lp.stats

    columns = ['responseSuccessCount',
               'responseErrorCount',
               'requestRedirectCount',
               'pageLoadTimeoutCount',
               'nonHtmlResponseCount',
               'networkErrorCount']
    data = [stats[x] for x in columns]

    file_name = "index.html"
    create_pie_chart(columns, data).render("templates/" + file_name)

    return render_template(file_name)


@app.route('/statistics/item/<name>')
def item(name):
    lp = LogProcess()
    stats = lp.stats

    columns = ['filteredDuplicateItemCount',
               'parseErrorCount',
               'parseItemCount',
               ]
    data = [stats[x] for x in columns]

    file_name = "index.html"
    create_pie_chart(columns, data).render("templates/" + file_name)

    return render_template(file_name)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
