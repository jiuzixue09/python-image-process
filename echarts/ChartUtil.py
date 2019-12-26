import pyecharts.options as opts
from pyecharts.charts import Line, Pie, Bar

from echarts.LogParse import LogParse


def create_line_chart(xaxis, yaxis_pair, title='') -> Line:
    c = Line(init_opts=opts.InitOpts(width="90%")).add_xaxis(xaxis)

    for pair in yaxis_pair:
        c.add_yaxis(pair[0], pair[1], stack=True, markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
                opts.MarkPointItem(type_="average", name="平均值"),
            ]
        ))

    c.set_global_opts(
        title_opts=opts.TitleOpts(title=title, pos_top="48%"),
        legend_opts=opts.LegendOpts(pos_top="5%"),
        datazoom_opts=[opts.DataZoomOpts()]
    )

    return c


def create_bar_chart(xaxis, yaxis_pair, title='') -> Line:
    c = Bar(init_opts=opts.InitOpts(width="90%")).add_xaxis(xaxis)

    for pair in yaxis_pair:
        c.add_yaxis(pair[0], pair[1], stack=True, markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
                    opts.MarkPointItem(type_="average", name="平均值"),
                ]
            ))

    c.set_global_opts(
        title_opts=opts.TitleOpts(title=title, pos_top="48%"),
        legend_opts=opts.LegendOpts(pos_top="5%"),
        datazoom_opts=[opts.DataZoomOpts()],
    )
    c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    return c


def create_pie_chart(*data_pair, series_name=None, title="") -> Pie:
    p = Pie(init_opts=opts.InitOpts(width="90%"))

    if len(data_pair) > 1:
        for index, pair in enumerate(data_pair):
            p.add(series_name, pair, center=[str((index + 1) * 35) + "%", "50%"], radius=[0, 300 / len(data_pair)])
    else:
        p.add(series_name, data_pair[0], radius=[0, 300])

    p.set_global_opts(title_opts=opts.TitleOpts(title=title),
                      legend_opts=opts.LegendOpts(pos_left="5%")) \
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

    return p
