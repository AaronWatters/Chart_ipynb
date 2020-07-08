from . import chart_framework
from . import utils
import pandas as pd
import numpy as np
import random


class Chart_init(chart_framework.ChartSuperClass):

    title = 'Chart'
    chart_type = 'line'

    def __init__(self, options=None, title = None, *pargs, **kwargs):
        super(Chart_init, self).__init__(*pargs, **kwargs)
        if options is None:
            options = self.default_options()
        if title is not None:
            self.title = title
        self.options = options
        self.labels = []
        self.data = []
        self.colors = []
        self.datasets = []
        self.dataset_name = []
        self.remove_item = []
    
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

    def get_ready_data(self, label, backgroundColor=None, borderColor=None, fill = False, **other_arguments):
        """
        if need more settings when single data is added
        """
        if self.colors:
            if backgroundColor is None:
                backgroundColor = self.colors
            if borderColor is None:
                borderColor = self.colors
        self.add_dataset(self.labels, self.data, label, 
                        backgroundColor = backgroundColor, 
                        borderColor = borderColor, 
                        fill = fill,
                        **other_arguments,
                        )

    def setup(self, width=800, **other_arguments): 
        if not self.datasets:
            self.add_dataset(self.labels, self.data, "My dataset", color=self.colors)
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

    def update_axis_type(self, axis_position, axis_type):
        '''
        axis_position: 'x', 'y'
        axis_type: 'category', 'logarithmic', 'linear'
        '''
        axis_name = {'x': 'xAxes', 'y': 'yAxes'}
        axis_po = axis_name[axis_position]
        if 'scales' in self.options:
            if axis_po in self.options['scales']:
                if 'type' in self.options['scales'][axis_po][0]:
                    self.options['scales'][axies_po][0]['type'] = axis_type
                else:
                    self.options['scales'][axis_po][0].update({'type':axis_type})
            else:
                self.options['scales'].update({axis_po:[{'type':axis_type}]})
        else:
            self.options.update({'scales':{axis_po:[{'type':axis_type}]}})

    def update_data(self, data_value, label):
        self.labels.append(label)
        self.js_init("""
            element.chart_info.chart.config.data.datasets[0].data.push(data_value);
            element.chart_info.chart.config.data.labels.push(label);
            element.chart_info.chart.update();
        """, data_value = data_value, label = label)

    def update_dataset(self, data, label=None, color = None, backgroundColor=None, borderColor=None, **other_arguments):
        
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
        if label is None:
            label = 'newDataset'

        dataset = utils.dataset(backgroundColor = backgroundColor, 
                    borderColor = borderColor,
                    data = data,
                    label = label,
                    **other_arguments,)
        self.datasets.append(dataset)
        self.js_init("""
            element.chart_info.chart.config.data.datasets.push(dataset)
            element.chart_info.chart.update();
        """, dataset = dataset)

    def remove_data(self):

        def callback_info(info, remove_label):
            self.remove_item.append(info)
            self.datasets[info['datasetIndex']]['data'].pop(info['dataIndex'])
            if remove_label:
                self.labels.pop(info['dataIndex'])


        self.js_init("""
            var canvas = element.chart_info.canvas;
            var chart = element.chart_info.chart;
            var canvas0 = canvas[0];
            canvas0.onclick = function(event) {
                var remove_info = {};
                var data = chart.getElementAtEvent(event);
                console.log(data[0]);
                var index = data[0]._index;
                var dataset_index = data[0]._datasetIndex;
                
                var chart_info = data[0]._chart;
                var chart_config = chart_info.config;
                var datasets = chart_config.data.datasets;
                var labels = chart_config.data.labels;
                var dataset = datasets[dataset_index];

                dataset.data.splice(index,1);
                var total_len = 0;
                var remove_label = false;
                for (var i = 0; i < datasets.length; i++){
                    total_len += datasets[i].data.length;
                }

                if ((total_len/3) == (labels.length-1)){
                    labels.splice(index,1);
                    remove_label = true;
                }

                remove_info.dataIndex = index;
                remove_info.datasetIndex = dataset_index;
                element.chart_info.chart.update();
                callback_info(remove_info, remove_label);
            };
        """, callback_info = callback_info)