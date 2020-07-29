from . import chart_framework
from . import chart_setup
from . import utils
import pandas as pd
import numpy as np


class Bar(chart_setup.Chart_init):
    
    title = 'Bar Chart'
    chart_type = 'bar'

    def __init__(self, options=None, stacked = False, title = None, *pargs, **kwargs):
        super(Bar, self).__init__(title = title, *pargs, **kwargs)
        if options is None:
            options = utils.options(
					responsive=True,
                    legend=dict(position="top"),
                    title=dict(display=True, text=self.title),
					tooltips = dict(mode='index', intersect = False),
					scales = utils.scales(xAxes=[dict(stacked = stacked)],
                                          yAxes=[dict(stacked = stacked)])
            )
        self.options = options
        self.reset()

def bar_chart(title, data, label=None, value=None):
    '''
    data format: pd.DataFrame 
                 or
                 {'label1': 1, 'label2': 2}
                 or
                 {'label':[], 'dataset1':[],...}
    '''
    chart = Bar(title=title)
    if isinstance(data, pd.DataFrame):
        if (label is not None) & (value is not None):
            data = data[[label,value]].groupby(label).count().reset_index()
            label = data[label].tolist()
            value = data[value].tolist()
        chart.add_dataset(label,value,'dataset1')
    if isinstance(data, dict):
        if 'label' in data:
            label = data['label']
            data.pop('label')
            for name, val in data:
                chart.add_dataset(label, val, name)
        else:
            label = list(data.keys())
            value = list(data.values())
            chart.add_dataset(label,value,'dataset1')
    chart.setup()
    return chart

            


    