from . import chart_framework
from . import chart_setup
from . import utils
import pandas as pd
import numpy as np
import random


class Line(chart_setup.Chart_init):

    title = 'Line Chart'
    chart_type = 'line'

    def __init__(self, options=None, title = None, *pargs, **kwargs):
        super(Line, self).__init__(title = title, *pargs, **kwargs)
        if options is None:
            options = self.default_options()
        self.options = options
        self.reset()


    def default_options(self):
        true = True
        options = utils.options(
            responsive=true,
            legend=dict(position="top"),
            title=dict(display=true, text=self.title),
            animation=dict(animateScale=true, animateRotate=true),
            scales = utils.scales(
                        xAxes = [utils.axes(
                                display = True,
                                scaleLabel = dict(display=true, labelString='x')
                            )],
                        yAxes = [utils.axes(
                                display = True,
                                scaleLabel = dict(display=true, labelString='y'),
                                ticks = {'min':0},
                        )]
                    )
        )
        self.options = options
        return options

def line_chart(title, data, label=None, value=None):
    '''
    data format: pd.DataFrame 
                 or
                 {'label1': 1, 'label2': 2}
                 or
                 {'label':[], 'dataset1':[],...}
    '''
    chart = Line(title=title)
    if isinstance(data, pd.DataFrame):
        if (label is not None) & (value is not None):
            data = data[[label,value]].groupby(label).sum().reset_index()
            label = data[label].tolist()
            value = data[value].tolist()
        chart.add_dataset(label,value,'dataset1')
    if isinstance(data, dict):
        if 'label' in data:
            label = data['label']
            data.pop('label')
            for name in data:
                chart.add_dataset(label, data[name], name)
        else:
            label = list(data.keys())
            value = list(data.values())
            chart.add_dataset(label,value,'dataset1')
    chart.setup()
    return chart