from . import chart_framework
from . import utils
import pandas as pd
import numpy as np


class Chart_init(chart_framework.ChartSuperClass):

    title = 'Chart'
    chart_type = 'line'

    def __init__(self, options=None, *pargs, **kwargs):
        super(Chart_init, self).__init__(*pargs, **kwargs)
        if options is None:
            options = self.default_options()
        self.options = options
        self.labels = []
        self.data = []
        self.colors = []
        self.datasets = []
        self.dataset_name = []
    
    def add(self, label, datum, color):
        self.labels.append(label)
        self.data.append(datum)
        self.colors.append(color)

    def add_dataset(self, data_x, data_y, dataset_name, color = None, 
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
        self.colors.append(color)
        self.labels = data_x

        _dataset = utils.dataset(
                        label=dataset_name,
                        data=data_y,
                        backgroundColor = backgroundColor,
                        borderColor = borderColor,
                        fill = fill,
                        **other_arguments,
                    )
        self.datasets.append(_dataset)

    def get_ready_data(self, label, backgroundColor, borderColor, fill = False, **other_arguments):
        """
        if need more settings when single data is added
        """
        self.add_dataset(self.labels, self.data, label, 
                        backgroundColor = backgroundColor, 
                        borderColor = borderColor, 
                        fill = fill,
                        **other_arguments,
                        )

    def setup(self, width=800, **other_arguments): 
        if not self.datasets:
            self.add_dataset(self.labels, self.data, "My dataset")
        config = utils.config(
            type=self.chart_type,
            data=utils.data(
                datasets=self.datasets,
                labels = self.labels,
            ),
            options=self.options,
            **other_arguments,
        )
        self.initialize_chart(width, config)

    def reset(self):
        self.labels = []
        self.data = []
        self.colors = []
        self.datasets = []
        self.dataset_name = []