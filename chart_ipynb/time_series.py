from . import chart_framework
from . import chart_setup
from . import utils, line, bar
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

def default_axis(axis, axis_label = None, multi_axis = False, multi_axis_name = None, stacked = False):
        axis_labels = {'x': 'x', 'y': 'y'}
        if axis_label is None:
            axis_label = axis_labels[axis]
        if stacked:
            return {'stacked': True}
        if axis == 'x':
            return utils.axes(
                display=True,
                scaleLabel = dict(display = True, labelString = axis_label),
                ticks = dict(
                    major = {
                            'enabled': True,
                            'fontStyle': 'bold'
                            },
                    source = 'data'
                ),
            )
        else:
            if multi_axis:
                if multi_axis_name is None:
                    multi_axis_name = ['dataset1', 'dataset2']
                axis_label_1 = axis_label + ' : ' + multi_axis_name[0]
                axis_label_2 = axis_label + ' : ' + multi_axis_name[1]
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

def ts_default_option(xAxes = None, yAxes = None, 
                       xAxes_name = None, yAxes_name = None,
                       multi_axis = False, multi_axis_name = None,
                       stacked = False, title = None):

        if xAxes is None:
            if xAxes_name is None:
                xAxes_name = 'Date'
            xAxes = default_axis('x', axis_label = xAxes_name, stacked = stacked)
        if yAxes is None:
            yAxes = default_axis('y', axis_label = yAxes_name, 
                                 multi_axis = multi_axis, multi_axis_name = multi_axis_name, stacked = stacked)
        _option = utils.options(
                        responsive=True,
                        title=dict(display=True, text=title),
                        animation = dict(duration=0),
                        scales = { 'xAxes': xAxes, 'yAxes': yAxes}
                )
        if stacked:
            _option = utils.options(
                        responsive=True,
                        title=dict(display=True, text=title),
                        tooltips= {
                            'mode': 'index',
                            'intersect': False
                        },
                        scales = {
                                    'xAxes': [{
                                        'stacked': True,
                                    }],
                                    'yAxes': [{
                                        'stacked': True
                                    }]
                                }
                )
                
        return _option

def time_series_Chart(_chart_type, ticker_symbol, val_col, date_col = None, start=None, end=None, 
                            data_provide = False, input_dataset = None,
                            website = None, api_key = None, 
                            multi_axis = False, axis_label = None, stacked = False,
                            options = None, xAxes = None, yAxes = None,
                            colors=None, backgroundColor = None, borderColor = None, 
                            title = None,
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
        options = ts_default_option(xAxes = xAxes, yAxes = yAxes, 
                                    yAxes_name = val_col, 
                                    multi_axis = multi_axis, multi_axis_name=ticker_symbol, stacked = stacked, title = title)

    result = None
    if _chart_type == 'line':
        result = line.Line(options = options, title=title)
    if _chart_type == 'bar':
        result = bar.Bar(options = options, stacked=stacked, title=title)


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
                if stacked:
                    result.add_dataset(result.labels, _data, symbol, color = colors[i],
                                    backgroundColor = backgroundColor[i], 
                                    borderColor = borderColor[i])
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