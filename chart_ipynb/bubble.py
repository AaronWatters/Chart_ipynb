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