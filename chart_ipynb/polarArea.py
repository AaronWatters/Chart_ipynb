from . import chart_framework
from . import chart_setup
from . import utils
import pandas as pd
import numpy as np


class PolarArea(chart_setup.Chart_init):
    
    title = 'Polar Area Chart'
    chart_type = 'polarArea'

    def __init__(self, options=None, title = None,  *pargs, **kwargs):
        super(PolarArea, self).__init__(title=title, *pargs, **kwargs)
        if options is None:
            self.options = utils.options(
					responsive=True,
                    legend=dict(position="top"),
                    title=dict(display=True, text=self.title),
					tooltips = dict(mode='index', intersect = False),
					scales = utils.scales(ticks = {'beginAtZero': True,'reverse': False}),
                    animation = dict(animateRotate = False, animateScale = True)
            )
        self.options = options
        self.reset()
