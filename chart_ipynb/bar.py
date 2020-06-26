from . import chart_framework
from . import utils, line
import pandas as pd
import numpy as np


class Bar(line.Line):
    
    title = "Bar Chart"
    chart_type = 'line'

    def __init__(self, options=None, stacked = False, *pargs, **kwargs):
        super(Bar, self).__init__(*pargs, **kwargs)
        if options is None:
            self.options = utils.options(
					title = {
						'display': True,
						'text': self.title
					},
                    legend = {
						'position': 'top',
					},
					tooltips = {
						'mode': 'index',
						'intersect': False
					},
					responsive = True,
					scales = {
						'xAxes': [{
							'stacked': stacked,
						}],
						'yAxes': [{
							'stacked': stacked,
						}]
					}
            )

    def set_dataset(self, multi_axis = False, **others):
        _datasets = []
        if len(self.datasets) >= 1:
            if not multi_axis:
                _data_list = list(self.datasets.items())
                for i in range(len(self.datasets)):
                    _label = _data_list[i][0]
                    _data = _data_list[i][1]
                    d = utils.dataset(
                        label=_label,
                        data=_data,
                        backgroundColor=utils.color_rgb(self.colors[_label],0.5),
                        borderColor = utils.color_rgb(self.colors[_label]),
                        borderWidth = 1,
                        **others,
                    )
                    _datasets.append(d)
            else:
                if len(self.datasets) != 2:
                    raise 'multi axis only applies to two datasets'
                _data_list = list(self.datasets.items())
                for i in range(len(self.datasets)):
                    _label = _data_list[i][0]
                    _data = _data_list[i][1]
                    d = utils.dataset(
                        label=_label,
                        data=_data,
                        yAxisID = 'y-axis-'+str(i+1),
                        backgroundColor=utils.color_rgb(self.colors[_label],0.5),
                        borderColor = utils.color_rgb(self.colors[_label]),
                        borderWidth = 1,
                        **others
                    )
                    _datasets.append(d)

        else:
            _datasets = [
                utils.dataset(
                        label="My dataset",
                        data=self.data,
                        backgroundColor=self.colors,
                        **others,
                    )
            ] 
        return _datasets
    
    def setup(self, width=800, multi_axis = False, _dataset = None, 
                **other_arguments): 
        if _dataset is None:
            _datasets = self.set_dataset(multi_axis = multi_axis)
        config = utils.config(
            type="bar",
            data=utils.data(
                datasets=_datasets,
                labels = self.labels,
            ),
            options=self.options,
            **other_arguments,
        )
        self.initialize_chart(width, config)
    
    