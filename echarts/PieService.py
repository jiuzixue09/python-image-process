from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Pie


def create_pie_chart(columns, data, series_name=None, title="") -> Pie:
    p = Pie()\
        .add(series_name, [list(z) for z in zip(columns, data)], center=["55%", "50%"]) \
        .set_global_opts(title_opts=opts.TitleOpts(title=title), legend_opts=opts.LegendOpts(pos_left="25%"))\
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

    return p


if __name__ == '__main__':
    columns = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    data = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
    create_pie_chart(columns, data, title="基本示例").render()
