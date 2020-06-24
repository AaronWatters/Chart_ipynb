from . import chart_framwork
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
        self.dataset_label = []
    
    def add(self, label, datum):
        self.labels.append(label)
        self.data.append(datum)

    def add_dataset(self, data, dataset_label, color):
        self.dataset_label.append(dataset_label)
        self.datasets[dataset_label] = data
        self.colors[dataset_label] = color

    def setup(self, width=800):
        _datasets = []
        if len(self.datasets) > 1:
            _data_list = list(self.datasets.items())
            for i in range(len(self.datasets)):
                _label = _data_list[i][0]
                _data = _data_list[i][1]
                d = utils.dataset(
                    label=_label,
                    data=_data,
                    backgroundColor=utils.color_rgb[self.colors[_label]],
                    fill = False
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
        )
        self.initialize_chart(width, config)




def time_series_example(ticker_symbol, start, end, col):
    '''
    ticker_symbol: stock symbol for company; a list or a string
    start, end: 'year-month-day'
    col: price type
    '''
    import pandas_datareader
    import pandas_datareader.data as web
    import datetime
    import time

    result = Line()
    result.set_title("Closing Prices")
    api_key = '1JFowowyzc-FnajAsDkY'
    s_split = [int(d) for d in start.split('-')]
    e_split = [int(d) for d in end.split('-')]
    start = datetime.datetime(s_split[0],s_split[1],s_split[2])
    end = datetime.datetime(e_split[0],e_split[1],e_split[2])
    if isinstance(ticker_symbol, str):
        ticker_symbol = [ticker_symbol]
    for i in range(len(ticker_symbol)):
            symbol = ticker_symbol[i]
            _dataset = web.DataReader(symbol,"quandl", start, end, api_key = api_key)
            _data, _data_label = data_format(_dataset, col)
            result.add_dataset(_data, _data_label, 'red')
    result.setup()
    return result



