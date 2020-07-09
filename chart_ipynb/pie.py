from . import chart_framework
from . import chart_setup
from . import utils
import pandas as pd
import numpy as np


class Pie(chart_setup.Chart_init):
    
    title = 'Pie Chart'
    chart_type = 'pie'

    def __init__(self, options=None, title = None,  *pargs, **kwargs):
        super(Pie, self).__init__(title=title, *pargs, **kwargs)
        if options is None:
            options = self.default_options()
        self.options = options
        self.reset()
