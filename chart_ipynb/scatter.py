from . import chart_framework
from . import chart_setup
from . import utils
import pandas as pd
import numpy as np


class Scatter(chart_setup.Chart_init):

    title = 'Scatter Chart'
    chart_type = 'scatter'

    def __init__(self, options=None, title = None, *pargs, **kwargs):
        super(Scatter, self).__init__(title = title, *pargs, **kwargs)
        if options is None:
            options = self.default_options()
        self.options = options
        self.reset()

    def add(self, datum, color):
        self.data.append(datum)
        self.colors.append(color)

    def add_dataset(self, data, dataset_name, color = None, 
                    backgroundColor = None, borderColor = None, 
                    fill = False,
                    **other_arguments,
        ):
        import random
        
        if color is None:
            if backgroundColor is not None:
                color = backgroundColor
            elif borderColor is not None:
                color = borderColor
            else:
                color = random.choice(utils.color_name)
        if backgroundColor is None:
            backgroundColor = color
        if borderColor is None:
            borderColor = color
        
        self.dataset_name.append(dataset_name)


        _dataset = utils.dataset(
                        label=dataset_name,
                        data=data,
                        backgroundColor = backgroundColor,
                        borderColor = borderColor,
                        fill = fill,
                        **other_arguments,
                    )
        self.datasets.append(_dataset)

    def get_ready_data(self, label, backgroundColor=None, borderColor=None, fill = False, **other_arguments):
        """
        if need more settings when single data is added
        """
        if self.colors:
            if backgroundColor is None:
                backgroundColor = self.colors
            if borderColor is None:
                borderColor = self.colors
        self.add_dataset(self.data, label, 
                        backgroundColor = backgroundColor, 
                        borderColor = borderColor, 
                        fill = fill,
                        **other_arguments,
                        )

    def setup(self, width=800, **other_arguments): 
        if not self.datasets:
            self.add_dataset(self.data, "My dataset", backgroundColor = self.colors)
        config = utils.config(
            type=self.chart_type,
            data=utils.data(
                datasets=self.datasets,
            ),
            options=self.options,
            **other_arguments,
        )
        self.initialize_chart(width, config)
    