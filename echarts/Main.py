from flask import Flask, request, send_from_directory

from echarts.PieService import create_pie_chart

app = Flask(__name__)


@app.route('/test')
def im_url_to_phash():
    # name = request.args.get("name")

    columns = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    data = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
    file_name = "index.html"
    create_pie_chart(columns, data).render(file_name)

    return send_from_directory('', file_name)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
