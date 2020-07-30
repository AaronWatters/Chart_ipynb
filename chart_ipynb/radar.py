from . import chart_framework
from . import chart_setup
from . import utils
import pandas as pd
import numpy as np
import random


class Radar(chart_setup.Chart_init):
    
    title = 'Radar Chart'
    chart_type = 'radar'

    def __init__(self, options=None, title = None, *pargs, **kwargs):
        super(Radar, self).__init__(title = title, *pargs, **kwargs)
        if options is None:
            options = utils.options(
					responsive=True,
                    legend=dict(position="top"),
                    title=dict(display=True, text=self.title),
					tooltips = dict(mode='index', intersect = False),
					scales = utils.scales(ticks = {'beginAtZero': True})
            )
        self.options = options
        self.reset()

def radar_chart(title, data, label=None, value=None, agg=None):
    '''
    data format: pd.DataFrame 
                 or
                 {'label1': 1, 'label2': 2}
                 or
                 {'label':[], 'dataset1':[],...}
    '''
    chart = Radar(title=title)
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