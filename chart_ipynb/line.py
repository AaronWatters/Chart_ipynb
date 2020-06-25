from . import chart_framework
from . import utils
import pandas as pd
import numpy as np


def data_format(dataset, val_col, data_provide = False, date_col=None):
        """
        dataset: pd.DataFrame
        val_col: the column name for the target value. e.g 'Close'
        """
        if not data_provide:
            date_col = 'Date'
        else:
            if date_col is None:
                print('please specify the date column')
                raise
        idx_reset_df = dataset.reset_index()
        data = idx_reset_df[[val_col, date_col]]
        sort_df = idx_reset_df.sort_values(by=date_col)
        sort_df[date_col]=sort_df[date_col].astype(str)

        return  list(sort_df[val_col]), list(sort_df[date_col])


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

    def set_dataset(self, multi_axis = False, **others):
        _datasets = []
        if len(self.datasets) >= 1:
            if not multi_axis:
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
                        borderWidth = 2,
                        **others,
                    )
                    _datasets.append(d)
            else:
                if len(self.datasets) != 2:
                    raise 'multi axis only applies to two datasets'
                _data_list = list(self.datasets.items())
                for i in range(len(self.datasets)):
                    _label = _data_list[i][0]
                    _data = _data_list[i][1]
                    d = utils.dataset(
                        label=_label,
                        data=_data,
                        yAxisID = 'y-axis-'+str(i+1),
                        backgroundColor=utils.color_rgb(self.colors[_label],0.5),
                        borderColor = utils.color_rgb(self.colors[_label]),
                        fill = False,
                        type = 'line',
                        pointRadius = 0,
                        lineTension = 0,
                        borderWidth = 2,
                        **others,
                    )
                    _datasets.append(d)

        else:
            _datasets = [
                utils.dataset(
                        label="My dataset",
                        data=self.data,
                        backgroundColor=self.colors,
                        **others,
                    )
            ] 
        return _datasets

    def setup(self, width=800, multi_axis = False, _dataset = None, 
                **other_arguments): 
        if _dataset is None:
            _datasets = self.set_dataset(multi_axis = multi_axis)
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




def time_series_lineChart(ticker_symbol, val_col, start=None, end=None, colors=None, 
                        data_provide = False, input_dataset = None, date_col = None,
                        website = None, api_key = None, 
                        multi_axis = False, axis_label = None,
                        width=800,
                        fontStyle = 'bold', 
                        autoSkip=True, autoSkipPadding = 10, maxRotation = 60,
                        **other_arguments
                    ):
    '''
    ticker_symbol: stock symbol for company; a list or a string
                    if self provide data, should be the name list or string of the dataset
    start, end: 'year-month-day'
    val_col: price type
    colors: colors for dataset; one for each
    multi_axis: only for two datasets
    data_provide: if or not self provide data
    website: the address to get data
    api_key: api key to access the data at website
    input_dataset: a list
    '''
    import pandas_datareader
    import pandas_datareader.data as web
    import datetime
    import time
    import random
    
    if not data_provide:   
        if website == 'quandl' and api_key is None:
            api_key = '1JFowowyzc-FnajAsDkY'
        s_split = [int(d) for d in start.split('-')]
        e_split = [int(d) for d in end.split('-')]
        start = datetime.datetime(s_split[0],s_split[1],s_split[2])
        end = datetime.datetime(e_split[0],e_split[1],e_split[2])
    else:
        if input_dataset is None or date_col is None:
            print('please enter your data and specify the date column')
            raise

    if axis_label is None:
        axis_label = val_col.capitalize()

    if not multi_axis:
        options = utils.options(
                responsive = True,
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
                            'labelString': axis_label
                        }
                    }]
                },
            )
    else:
        if isinstance(ticker_symbol, str) or len(ticker_symbol) != 2:
            raise 'multi axis only applies to two datasets'

        options = utils.options(
                responsive = True,
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
                        'type': 'linear',
                        'display': True,
                        'position': 'left',
                        'id': 'y-axis-1',
                        'gridLines': {
                            'drawBorder': False
                        },
                        'scaleLabel': {
                            'display': True,
                            'labelString': axis_label
                        }
                    },{
                        'type': 'linear',
                        'display': True,
                        'position': 'right',
                        'id': 'y-axis-2',
                        'gridLines': {
                            'drawOnChartArea': False
                        },
                        'scaleLabel': {
                            'display': True,
                            'labelString': axis_label
                        }
                    }]
                },
            )

    result = Line(options = options)
    if isinstance(ticker_symbol, str):
        ticker_symbol = [ticker_symbol]
    if colors is None:
        colors = [random.choice(utils.color_name) for i in range(len(ticker_symbol))]
    for i in range(len(ticker_symbol)):
            symbol = ticker_symbol[i]
            _dataset = None
            if not data_provide:
                _dataset = web.DataReader(symbol, website, start, end, api_key = api_key)
            else:
                _dataset = input_dataset[i]
            _data, result.labels = data_format(_dataset, val_col, 
                                                data_provide = data_provide, 
                                                date_col=date_col)
            result.add_dataset(_data, symbol, colors[i])

    result.setup(width, multi_axis = multi_axis, **other_arguments) 
        

    return result



