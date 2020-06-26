from . import chart_framework
from . import utils
import pandas as pd
import numpy as np


class Line(chart_framework.ChartSuperClass):

    title = "Line Chart"
    chart_type = 'line'

    def __init__(self, options=None, *pargs, **kwargs):
        super(Line, self).__init__(*pargs, **kwargs)
        if options is None:
            options = self.default_options()
        self.options = options
        self.labels = []
        self.data = []
        self.colors = []
        self.datasets = []
        self.dataset_name = []
    
    def add(self, label, datum):
        self.labels.append(label)
        self.data.append(datum)

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
        self.add_dataset(self.data, self.labels, label, 
                        backgroundColor = backgroundColor, 
                        borderColor = borderColor, 
                        fill = fill,
                        **other_arguments,
                        )

    def setup(self, width=800, **other_arguments): 
        if not self.datasets:
            self.add_dataset(self.data, self.labels, "My dataset")
        config = utils.config(
            type="line",
            data=utils.data(
                datasets=self.datasets,
                labels = self.labels,
            ),
            options=self.options,
            **other_arguments,
        )
        self.initialize_chart(width, config)

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