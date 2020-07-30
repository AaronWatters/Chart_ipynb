
from . import chart_framework
from . import chart_setup
from . import utils
import pandas as pd
import random

class Doughnut(chart_setup.Chart_init):

    title = "Doughnut Chart"
    chart_type="doughnut"

    def __init__(self, options=None, title = None, *pargs, **kwargs):
        super(Doughnut, self).__init__(title = title, *pargs, **kwargs)
        if options is None:
            options = self.default_options()
        self.options = options
        self.reset()
    

def example():
    result = Doughnut()
    result.set_title("Chocolate Frosted")
    result.add("Big", 10, "brown")
    result.add("Medium", 7, "pink")
    result.add("Small", 3, "purple")
    result.setup()
    return result

def doughnut_chart(title, data, label=None, value=None):
    '''
    data format: pd.DataFrame 
                 or
                 {'label1': 1, 'label2': 2}
                 or
                 {'label':[], 'dataset1':[],...}
    '''
    chart = Doughnut(title=title)
    if isinstance(data, pd.DataFrame):
        if (label is not None) & (value is not None):
            data = data[[label,value]].groupby(label).sum().reset_index()
            label = data[label].tolist()
            value = data[value].tolist()
            colors = [random.choice(utils.color_name) for i in label]
        chart.add_dataset(label,value,'dataset1',color=colors)
    if isinstance(data, dict):
        if 'label' in data:
            label = data['label']
            colors = [random.choice(utils.color_name) for i in label]
            data.pop('label')
            for name in data:
                chart.add_dataset(label, data[name], name, color=colors)
        else:
            label = list(data.keys())
            colors = [random.choice(utils.color_name) for i in label]
            value = list(data.values())
            chart.add_dataset(label,value,'dataset1', color=colors)
    chart.setup()
    return chart
