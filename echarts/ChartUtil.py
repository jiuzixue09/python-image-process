import pyecharts.options as opts
from pyecharts.charts import Line, Pie

from echarts.LogParse import LogParse


def create_line_chart(xaxis, yaxis_pair, title='') -> Line:
    c = Line(init_opts=opts.InitOpts(width="90%")).add_xaxis(xaxis)

    for pair in yaxis_pair:
        c.add_yaxis(pair[0], pair[1])

    c.set_global_opts(
        title_opts=opts.TitleOpts(title=title, pos_top="48%"),
        legend_opts=opts.LegendOpts(pos_top="5%"),
        datazoom_opts=[opts.DataZoomOpts()]
    )

    return c


def create_pie_chart(*data_pair, series_name=None, title="") -> Pie:
    p = Pie(init_opts=opts.InitOpts(width="90%"))

    if len(data_pair) > 1:
        for index, pair in enumerate(data_pair):
            p.add(series_name, pair, center=[str((index + 1) * 35) + "%", "50%"], radius=[0, 300 / len(data_pair)])
    else:
        p.add(series_name, data_pair[0], radius=[0, 300])

    p.set_global_opts(title_opts=opts.TitleOpts(title=title),
                      legend_opts=opts.LegendOpts(pos_left="5%", orient="vertical")) \
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

    return p
