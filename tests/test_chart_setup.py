import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from chart_ipynb import chart_framework, chart_setup, utils
import jp_proxy_widget

class TestChartInit(unittest.TestCase):

    @patch("chart_ipynb.chart_framework.load_requirements")
    def test_init(self, mock_load_requirements):
        widget = chart_setup.Chart_init()
        assert mock_load_requirements.called
        assert widget.title == 'Chart'
        assert widget.chart_type == 'line'

    
    def test_add(self):
        widget = chart_setup.Chart_init()
        widget.add('test',1,'red')
        assert len(widget.labels)==1
        assert len(widget.data)==1
        assert len(widget.colors)==1
        assert widget.labels[0]=='test'
        assert widget.data[0] == 1
        assert widget.colors[0] == 'red'

    def test_add_dataset(self):
        widget = chart_setup.Chart_init()
        arguments = {}
        def mock_add_dataset(**arg):
            arguments.update(arg)
        utils.dataset = mock_add_dataset
        widget.add_dataset('test',1,'test_name',color='red')
        expected_dataset = {'label': 'test_name', 'data': 1, 
                            'backgroundColor': 'red', 
                            'borderColor': 'red', 'fill': False}
        self.assertEqual(arguments, expected_dataset)
        assert len(widget.datasets)==1

    def test_get_ready_data(self):
        widget = chart_setup.Chart_init()
        arguments = {}
        def mock_add_dataset(*args, **kwargs):
            arguments.update(kwargs)
        widget.add_dataset = mock_add_dataset
        widget.get_ready_data('test', test_input='test')
        assert arguments['test_input']=='test'
        assert not widget.colors

    def test_setup(self):
        widget = chart_setup.Chart_init()
        arguments = {}
        def mock_config(**kwargs):
            arguments.update(kwargs)
        
        utils.config = mock_config
        widget.setup()
        expected_config = {'type': 'line', 
                          'data': {'datasets': [None], 'labels': []}, 
                          'options': {'responsive': True, 
                                      'legend': {'position': 'top'}, 
                                      'title': {'display': True, 'text': 'Chart'}, 
                                      'animation': {'animateScale': True, 'animateRotate': True}}}
        self.assertEqual(arguments, expected_config)

    def test_reset(self):
        widget = chart_setup.Chart_init()
        widget.add('test',1,'red')
        widget.setup()
        widget.reset()
        assert not widget.labels
        assert not widget.data
        assert not widget.colors
        assert not widget.datasets
        assert not widget.dataset_name

    def test_update_axis_type(self):
        widget = chart_setup.Chart_init()
        mock_arguments = {}
        widget.options = mock_arguments
        widget.update_axis_type('x','linear')
        expected_options = {'scales': {'xAxes': [{'type': 'linear'}]}}
        self.assertEqual(widget.options, expected_options)

    def test_update_data(self):
        widget = chart_setup.Chart_init()
        widget.datasets = [{'label':'test','data':[1]}]
        widget.labels = ['test']
        widget.dataset_name = ['test']
        widget.setup()
        arguments = {}
        def mock_js_init(*args, **kwargs):
            arguments.update(kwargs)
        widget.js_init = mock_js_init
        widget.update_data(2, 'test2')
        expected_change = {'data_value': 2, 
                          'label': 'test2', 
                          'dataset_index': 0, 
                          'add_label': True}
        self.assertEqual(arguments, expected_change)
        assert len(widget.datasets[0]['data'])==2

    @patch("chart_ipynb.utils.dataset")
    def test_update_dataset(self, mock_dataset):
        widget = chart_setup.Chart_init()
        widget.setup()
        widget.update_dataset([1,2,3])
        assert mock_dataset.called

    def test_remove_data(self):
        '''
        not implemented yet
        '''

    def test_remove_dataset(self):
        arguments = {}
        def mock_js_init(*args, **kwargs):
            arguments.update(kwargs)
        widget = chart_setup.Chart_init()
        widget.js_init = mock_js_init
        widget.dataset_name = ['test']
        widget.datasets = [{'test':1}]
        widget.remove_dataset('test')
        assert arguments['dataset_index']==0
        assert not widget.dataset_name
        assert not widget.datasets
        assert not widget.remove_dataset('test')
