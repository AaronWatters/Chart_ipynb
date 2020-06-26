from . import chart_framework
from . import utils
import pandas as pd
import numpy as np


class Line(chart_framework.ChartSuperClass):

    title = "Line Chart"
    chart_type = 'line'

    def __init__(self, options=None, *pargs, **kwargs):
        super(Line, self).__init__(*pargs, **kwargs)
        if options is None:
            options = self.default_options()
        self.options = options
        self.labels = []
        self.data = []
        self.colors = []
        self.datasets = []
        self.dataset_name = []
    
    def add(self, label, datum):
        self.labels.append(label)
        self.data.append(datum)

    def add_dataset(self, data_x, data_y, dataset_name, color = None, 
                    backgroundColor = None, borderColor = None, 
                    fill = False,
                    **other_arguments,
        ):
        import random
        
        if color is None:
            if backgroundColor is not None:
                color = backgroundColor
            elif borderColor is not None:
                color = borderColor
            else:
                color = random.choice(utils.color_name)
        if backgroundColor is None:
            backgroundColor = color
        if borderColor is None:
            borderColor = color
        
        self.dataset_name.append(dataset_name)
        self.colors.append(color)
        self.labels = data_x

        _dataset = utils.dataset(
                        label=dataset_name,
                        data=data_y,
                        backgroundColor = backgroundColor,
                        borderColor = borderColor,
                        fill = fill,
                        **other_arguments,
                    )
        self.datasets.append(_dataset)

    def get_ready_data(self, label, backgroundColor, borderColor, fill = False, **other_arguments):
        """
        if need more settings when single data is added
        """
        self.add_dataset(self.data, self.labels, label, 
                        backgroundColor = backgroundColor, 
                        borderColor = borderColor, 
                        fill = fill,
                        **other_arguments,
                        )

    def setup(self, width=800, **other_arguments): 
        if not self.datasets:
            self.add_dataset(self.data, self.labels, "My dataset")
        config = utils.config(
            type="line",
            data=utils.data(
                datasets=self.datasets,
                labels = self.labels,
            ),
            options=self.options,
            **other_arguments,
        )
        self.initialize_chart(width, config)

    def default_options(self):
        true = True
        options = utils.options(
            responsive=true,
            legend=dict(position="top"),
            title=dict(display=true, text=self.title),
            animation=dict(animateScale=true, animateRotate=true),
            scales = utils.scales(
                        xAxes = utils.axes(
                                display = True,
                                scaleLabel = dict(display=true, labelString='x')
                            ),
                        yAxes = utils.axes(
                                display = True,
                                scaleLabel = dict(display=true, labelString='y')
                            )
                    )
        )
        self.options = options
        return options


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

def time_series_lineChart(ticker_symbol, val_col, date_col = None, start=None, end=None, 
                            data_provide = False, input_dataset = None,
                            website = None, api_key = None, 
                            multi_axis = False, axis_label = None,
                            options = None, xAxes = None, yAxes = None,
                            colors=None, backgroundColor = None, borderColor = None, 
                            fill = False,
                            width=800,
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
    
    def default_axis(axis, multi_axis = False):
        if axis == 'x':
            return utils.axes(
                display=True,
                scaleLabel = dict(display = True, labelString = 'Date'),
                ticks = dict(
                    major = {
                            'enabled': True,
                            'fontStyle': 'bold'
                            },
                    source = 'data',
                    autoSkip = True,
                    autoSkipPadding = 10,
                    maxRotation =  60
                ),
            )
        else:
            if multi_axis:
                axis_label_1 = ticker_symbol[0] + ' : ' + axis_label
                axis_label_2 = ticker_symbol[1] + ' : ' + axis_label
                return [utils.axes(
                            display = True,
                            scaleLabel = {
                                'display': True,
                                'labelString': axis_label_1
                                },
                            type = 'linear',
                            position = 'left',
                            id = 'y-axis-1',
                            gridLines = {
                                'drawBorder': False
                            }
                        ), utils.axes(
                            display = True,
                            scaleLabel = {
                                'display': True,
                                'labelString': axis_label_2
                                },
                            type = 'linear',
                            position = 'right',
                            id = 'y-axis-2',
                            gridLines = {
                                'drawBorder': False,
                                'drawOnChartArea': False
                            }
                        )]
            else:
                return [utils.axes(
                            display = True,
                            scaleLabel = {
                                'display': True,
                                'labelString': axis_label
                                },
                            gridLines = {
                                'drawBorder': False
                            }
                        )]
    
    def default_option(xAxes = None, yAxes = None, multi_axis = False):
        if xAxes is None:
            xAxes = default_axis('x')
        if yAxes is None:
            yAxes = default_axis('y', multi_axis = multi_axis)
        _option = utils.options(
                        responsive=True,
                        animation = dict(duration=0),
                        scales = { 'xAxes': xAxes, 'yAxes': yAxes}
                )
        return _option



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

    if isinstance(ticker_symbol, str):
        ticker_symbol = [ticker_symbol]
    if multi_axis and len(ticker_symbol) != 2:
        print('multi axis only applies to two datasets')
        raise

    if colors is None:
            if backgroundColor is not None:
                colors = backgroundColor
            elif borderColor is not None:
                colors = borderColor
            else:
                colors = [None for i in range(len(ticker_symbol))]
    if backgroundColor is None:
        backgroundColor = colors
    if borderColor is None:
        borderColor = colors

    if options is None:
        options = default_option(xAxes = xAxes, yAxes = yAxes, multi_axis = multi_axis)
    result = Line(options = options)
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
            if multi_axis:
                result.add_dataset(result.labels, _data, symbol, color = colors[i],
                                    backgroundColor = backgroundColor[i], 
                                    borderColor = borderColor[i], 
                                    fill = fill,
                                    yAxisID = 'y-axis-'+str(i+1),
                                    type = result.chart_type,
                                    pointRadius = 0,
                                    lineTension = 0,
                                    borderWidth = 1)
            else:
                result.add_dataset(result.labels, _data, symbol, color = colors[i],
                                    backgroundColor = backgroundColor[i], 
                                    borderColor = borderColor[i], 
                                    fill = fill,
                                    type = result.chart_type,
                                    pointRadius = 0,
                                    lineTension = 0,
                                    borderWidth = 1)
    result.setup(width, **other_arguments) 

    return result



