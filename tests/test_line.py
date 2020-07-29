import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from chart_ipynb import chart_framework, utils, line
import jp_proxy_widget

class TestLine(unittest.TestCase):

    @patch("chart_ipynb.chart_framework.load_requirements")
    @patch("chart_ipynb.utils.options")
    def test_init(self, mock_load_requirements, mock_options):
        widget = line.Line()
        assert mock_load_requirements.called
        assert mock_options.called
        assert widget.title == 'Line Chart'
        assert widget.chart_type == 'line'

    def test_default_options(self):
        widget = line.Line()
        options = widget.default_options()
        expected_options = {
            'responsive': True, 
            'legend': {'position': 'top'}, 
            'title': {'display': True, 'text': 'Line Chart'}, 
            'animation': {'animateScale': True, 'animateRotate': True}, 
            'scales': {
                'xAxes': [{'display': True, 
                            'scaleLabel': {'display': True, 'labelString': 'x'}, 
                            'stacked': False}], 
                'yAxes': [{'display': True, 
                            'scaleLabel': {'display': True, 'labelString': 'y'},
                            'ticks':{'min':0},
                            'stacked': False}]}}
        self.assertEqual(options, expected_options)
