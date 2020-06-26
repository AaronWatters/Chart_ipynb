from . import chart_framework
from . import chart_setup
from . import utils
import pandas as pd
import numpy as np


class Line(chart_setup.Chart_init):

    title = 'Line Chart'
    chart_type = 'line'

    def __init__(self, options=None, *pargs, **kwargs):
        super(Line, self).__init__(*pargs, **kwargs)
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
                        xAxes = utils.axes(
                                display = True,
                                scaleLabel = dict(display=true, labelString='x')
                            ),
                        yAxes = utils.axes(
                                display = True,
                                scaleLabel = dict(display=true, labelString='y')
                            )
                    )
        )
        self.options = options
        return options