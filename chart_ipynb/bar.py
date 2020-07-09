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


    