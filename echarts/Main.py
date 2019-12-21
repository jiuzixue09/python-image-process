from flask import Flask, render_template, request

from echarts.LogProcess import LogProcess
from echarts.PieService import create_pie_chart

app = Flask(__name__)


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
