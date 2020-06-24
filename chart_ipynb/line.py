from . import chart_framework
from . import utils
import pandas as pd
import numpy as np


def data_format(dataset, val_col):
        """
        dataset: pd.DataFrame
        val_col: the column name for the target value. e.g 'Close'
        """
        data = dataset[val_col]
        idx_reset_df = dataset.reset_index()
        if 'Date' not in idx_reset_df.columns:
            return 'please rename the date columns to "Date"'
        sort_df = idx_reset_df.sort_values(by='Date')
        sort_df['Date']=sort_df['Date'].astype(str)
        return  list(sort_df[val_col]), list(sort_df['Date'])


class Line(chart_framework.ChartSuperClass):

    title = "Line Chart"

    def __init__(self, options=None, *pargs, **kwargs):
        super(Line, self).__init__(*pargs, **kwargs)
        if options is None:
            options = self.default_options()
        self.options = options
        self.labels = []
        self.data = []
        self.colors = {}
        self.datasets = {}
        self.dataset_name = []
    
    def add(self, label, datum):
        self.labels.append(label)
        self.data.append(datum)

    def add_dataset(self, data, dataset_name, color):
        self.dataset_name.append(dataset_name)
        self.datasets[dataset_name] = data
        self.colors[dataset_name] = color

    def setup(self, width=800, **other_arguments):
        _datasets = []
        if len(self.datasets) >= 1:
            _data_list = list(self.datasets.items())
            for i in range(len(self.datasets)):
                _label = _data_list[i][0]
                _data = _data_list[i][1]
                d = utils.dataset(
                    label=_label,
                    data=_data,
                    backgroundColor=utils.color_rgb(self.colors[_label],0.5),
                    borderColor = utils.color_rgb(self.colors[_label]),
                    fill = False,
                    type = 'line',
                    pointRadius = 0,
                    lineTension = 0,
                    borderWidth = 2
                )
                _datasets.append(d)
        else:
            _datasets = [
                utils.dataset(
                        label="My dataset",
                        data=self.data,
                        backgroundColor=self.colors
                    )
            ] 
        config = utils.config(
            type="line",
            data=utils.data(
                datasets=_datasets,
                labels = self.labels,
            ),
            options=self.options,
            **other_arguments,
        )
        self.initialize_chart(width, config)




def time_series_stock(ticker_symbol, start, end, col, colors=None, width=800,
                        fontStyle = 'bold', 
                        autoSkip=True, autoSkipPadding = 10, maxRotation = 60,
                        **other_arguments
                    ):
    '''
    ticker_symbol: stock symbol for company; a list or a string
    start, end: 'year-month-day'
    col: price type
    '''
    import pandas_datareader
    import pandas_datareader.data as web
    import datetime
    import time
    import random

    options = utils.options(
            animation = {
                'duration': 0
            },
            scales = {
                'xAxes': [{
                    'display':True,
                    'scaleLabel':{
                        'display':True,
                        'labelString':'Date'
                    }
                    ,'ticks': {
                        'major': {
                            'enabled': True,
                            'fontStyle': fontStyle
                        },
                        'source': 'data',
                        'autoSkip': autoSkip,
                        'autoSkipPadding': autoSkipPadding,
                        'maxRotation': maxRotation,
                    },
                }],
                'yAxes': [{
                    'gridLines': {
                        'drawBorder': False
                    },
                    'scaleLabel': {
                        'display': True,
                        'labelString': col.capitalize() + ' price ($)'
                    }
                }]
            },
        )


    result = Line(options = options)
    api_key = '1JFowowyzc-FnajAsDkY'
    s_split = [int(d) for d in start.split('-')]
    e_split = [int(d) for d in end.split('-')]
    start = datetime.datetime(s_split[0],s_split[1],s_split[2])
    end = datetime.datetime(e_split[0],e_split[1],e_split[2])
    if isinstance(ticker_symbol, str):
        ticker_symbol = [ticker_symbol]
    if colors is None:
        colors = [random.choice(utils.color_name) for i in range(len(ticker_symbol))]
    for i in range(len(ticker_symbol)):
            symbol = ticker_symbol[i]
            _dataset = web.DataReader(symbol,"quandl", start, end, api_key = api_key)
            _data, result.labels = data_format(_dataset, col)
            result.add_dataset(_data, symbol, colors[i])
    result.setup(width, **other_arguments)
    return result



