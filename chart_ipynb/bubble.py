from . import chart_framework
from . import chart_setup
from . import scatter
from . import utils
import pandas as pd
import numpy as np


class Bubble(scatter.Scatter):

    title = 'Bubble Chart'
    chart_type = 'bubble'

    def __init__(self, options=None, title = None, *pargs, **kwargs):
        super(Bubble, self).__init__(title = title, *pargs, **kwargs)
        if options is None:
            options = self.default_options()
        self.options = options
        self.reset()

def bubble_chart(title, data, x=None, y=None):
    '''
    data format: pd.DataFrame 
                 or
                 [{'x': x,'y': y},{'x': x,'y': y},...]
                 or
                 {'x': [1,2,3], 'y': [2,4,6]}
                 or 
                 {'dataset1':[{'x':1,'y':2},...],
                  'dataset2':.....}
    '''
    chart = Bubble(title=title)
    if isinstance(data, pd.DataFrame):
        if x is not None:
            x = data[label].tolist()
        if y is not None:
            y = data[value].tolist()
        dataset = []
        for i in range(len(x)):
            d = {'x':x[i],'y':y[i]}
            dataset.append(d)
        chart.add_dataset(dataset,'dataset1')
    if isinstance(data, dict):
        if 'x' in data:
            x = data['x']
            y = data['y']
            dataset = []
            for i in range(len(x)):
                d = {'x':x[i],'y':y[i]}
                dataset.append(d)
            chart.add_dataset(dataset,'dataset1')
        else:
            for name, val in data:
                chart.add_dataset(val, name)
    if isinstance(data,list):
        chart.add_dataset(data, 'dataset1')
    chart.setup()
    return chart