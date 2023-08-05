import pandas as pd
from sqlalchemy import create_engine
from hbshare.rm_associated.config import engine_params
from datetime import datetime
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.globals import ThemeType


class EconomyMacro:
    def __init__(self, start_date='20050131', end_date='20210226'):
        self.start_date = start_date
        self.end_date = end_date
        self._load_data()

    def _load_data(self):
        sql_script = "SELECT * FROM macro_economy where TRADE_DATE >= {} and TRADE_DATE <= {}".format(
            self.start_date, self.end_date)
        engine = create_engine(engine_params)
        data = pd.read_sql(sql_script, engine)
        data['trade_date'] = data['trade_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))

        self.data = data[['trade_date', 'economy_increase', 'M1', 'M2', 'M1-M2', 'CPI', 'PPI']]

    def draw_picture_one(self):
        df = self.data[['trade_date', 'economy_increase']]
        line = Line(
            init_opts=opts.InitOpts(
                width='800px',
                height='500px',
                theme=ThemeType.WALDEN
            )
        ).set_global_opts(
            title_opts=opts.TitleOpts(title="经济增长"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_right="center", pos_top='5%'),
            xaxis_opts=opts.AxisOpts(
                type_='category',
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                axisline_opts=opts.AxisLineOpts(on_zero_axis_index=False),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        ).add_xaxis(
            xaxis_data=df['trade_date'].tolist()
        ).add_yaxis(
            series_name="经济增长",
            y_axis=df["economy_increase"].round(3).tolist(),
            is_symbol_show=False,
            label_opts=opts.LabelOpts(is_show=False)
        )

        return line

    def draw_picture_two(self):
        df = self.data[['trade_date', 'M1', 'M2', 'M1-M2']]
        line = Line(
            init_opts=opts.InitOpts(
                width='800px',
                height='500px',
                theme=ThemeType.WALDEN
            )
        ).set_global_opts(
            title_opts=opts.TitleOpts(title="宏观流动性"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_right="center", pos_top='5%'),
            xaxis_opts=opts.AxisOpts(
                type_='category',
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                axisline_opts=opts.AxisLineOpts(on_zero_axis_index=False),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        ).add_xaxis(
            xaxis_data=df['trade_date'].tolist()
        ).add_yaxis(
            series_name="M1",
            y_axis=df["M1"].round(3).tolist(),
            is_symbol_show=False,
            label_opts=opts.LabelOpts(is_show=False)
        ).add_yaxis(
            series_name="M2",
            y_axis=df["M2"].round(3).tolist(),
            is_symbol_show=False,
            label_opts=opts.LabelOpts(is_show=False)
        ).add_yaxis(
            series_name="M1-M2",
            y_axis=df["M1-M2"].round(3).tolist(),
            is_symbol_show=False,
            label_opts=opts.LabelOpts(is_show=False)
        )

        return line

    def draw_picture_three(self):
        df = self.data[['trade_date', 'CPI', 'PPI']]
        line = Line(
            init_opts=opts.InitOpts(
                width='800px',
                height='500px',
                theme=ThemeType.WALDEN
            )
        ).set_global_opts(
            title_opts=opts.TitleOpts(title="物价指数"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_right="center", pos_top='5%'),
            xaxis_opts=opts.AxisOpts(
                type_='category',
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                axisline_opts=opts.AxisLineOpts(on_zero_axis_index=False),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        ).add_xaxis(
            xaxis_data=df['trade_date'].tolist()
        ).add_yaxis(
            series_name="CPI",
            y_axis=df["CPI"].round(3).tolist(),
            is_symbol_show=False,
            label_opts=opts.LabelOpts(is_show=False)
        ).add_yaxis(
            series_name="PPI",
            y_axis=df["PPI"].round(3).tolist(),
            is_symbol_show=False,
            label_opts=opts.LabelOpts(is_show=False)
        )

        return line


class MarketMacro:
    def __init__(self, start_date='20120201', end_date='20210323'):
        self.start_date = start_date
        self.end_date = end_date
        self._load_data()

    def _load_data(self):
        sql_script = "SELECT * FROM market_macro where TRADE_DATE >= {} and TRADE_DATE <= {}".format(
            self.start_date, self.end_date)
        engine = create_engine(engine_params)
        data = pd.read_sql(sql_script, engine)
        data['trade_date'] = data['trade_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))

        self.data = data[['trade_date', 'wind_A', 'HS300', 'ZZ500']]

    def draw_picture(self):
        df = self.data.copy()
        line = Line(
            init_opts=opts.InitOpts(
                width='800px',
                height='500px',
                theme=ThemeType.WALDEN
            )
        ).set_global_opts(
            title_opts=opts.TitleOpts(title="市场宏观"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_right="center", pos_top='5%'),
            xaxis_opts=opts.AxisOpts(
                type_='category',
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                axisline_opts=opts.AxisLineOpts(on_zero_axis_index=False),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        ).add_xaxis(
            xaxis_data=df['trade_date'].tolist()
        ).add_yaxis(
            series_name="万得全A",
            y_axis=df["wind_A"].round(3).tolist(),
            is_symbol_show=False,
            is_smooth=True,
            linestyle_opts=opts.LineStyleOpts(width=1.5),
            label_opts=opts.LabelOpts(is_show=False)
        ).add_yaxis(
            series_name="沪深300",
            y_axis=df["HS300"].round(3).tolist(),
            is_symbol_show=False,
            is_smooth=True,
            linestyle_opts=opts.LineStyleOpts(width=1.5),
            label_opts=opts.LabelOpts(is_show=False)
        ).add_yaxis(
            series_name="中证500",
            y_axis=df["ZZ500"].round(3).tolist(),
            is_symbol_show=False,
            is_smooth=True,
            linestyle_opts=opts.LineStyleOpts(width=1.5),
            label_opts=opts.LabelOpts(is_show=False)
        )

        return line


class MarketMicro:
    def __init__(self, start_date='20050131', end_date='20210226'):
        self.start_date = start_date
        self.end_date = end_date
        self._load_data()

    def _load_data(self):
        sql_script = "SELECT * FROM market_micro where TRADE_DATE >= {} and TRADE_DATE <= {}".format(
            self.start_date, self.end_date)
        engine = create_engine(engine_params)
        data = pd.read_sql(sql_script, engine)
        data['trade_date'] = data['trade_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))

        self.left_data = data[data['direction'] == 'left'].sort_values(
            by='trade_date')[['trade_date', 'wind_A', 'HS300', 'ZZ500']]

        self.right_data = data[data['direction'] == 'right'].sort_values(
            by='trade_date')[['trade_date', 'wind_A', 'HS300', 'ZZ500']]

    def draw_picture(self, direction):
        if direction == 'left':
            df = self.left_data.copy()
            tl = "市场微观左侧"
        else:
            df = self.right_data.copy()
            tl = "市场微观右侧"

        line = Line(
            init_opts=opts.InitOpts(
                width='800px',
                height='500px',
                theme=ThemeType.WALDEN
            )
        ).set_global_opts(
            title_opts=opts.TitleOpts(title=tl),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_right="center", pos_top='5%'),
            xaxis_opts=opts.AxisOpts(
                type_='category',
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                axisline_opts=opts.AxisLineOpts(on_zero_axis_index=False),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        ).add_xaxis(
            xaxis_data=df['trade_date'].tolist()
        ).add_yaxis(
            series_name="万得全A",
            y_axis=df["wind_A"].round(3).tolist(),
            is_symbol_show=False,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False)
        ).add_yaxis(
            series_name="沪深300",
            y_axis=df["HS300"].round(3).tolist(),
            is_symbol_show=False,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False)
        ).add_yaxis(
            series_name="中证500",
            y_axis=df["ZZ500"].round(3).tolist(),
            is_symbol_show=False,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False)
        )

        return line


if __name__ == '__main__':
    # EconomyMacro('20050131', '20210226').draw_picture_three()
    # MarketMacro('20120201', '20210323').draw_picture()
    MarketMicro('20050131', '20210226').draw_picture(direction="right")
