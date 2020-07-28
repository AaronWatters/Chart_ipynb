import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from chart_ipynb import chart_framework, utils, doughnut
import jp_proxy_widget

class TestDoughnut(unittest.TestCase):

    @patch("chart_ipynb.chart_framework.load_requirements")
    @patch("chart_ipynb.utils.options")
    def test_init(self, mock_load_requirements, mock_options):
        widget = doughnut.Doughnut()
        assert mock_load_requirements.called
        assert mock_options.called
        assert widget.title == 'Doughnut Chart'
        assert widget.chart_type == 'doughnut'

    @patch("chart_ipynb.doughnut")
    def test_example(self, mock_doughnut):
        arguments = {}
        def mock_config(**args):
            arguments.update(args)
        utils.config = mock_config
        widget = doughnut.example()
        expected_config = {
            'type': 'doughnut', 
            'data': {
                'datasets': [None], 
                'labels': ['Big', 'Medium', 'Small']}, 
            'options': {'responsive': True, 
                        'legend': {'position': 'top'}, 
                        'title': {'display': True, 'text': 'Chocolate Frosted'}, 
                        'animation': {'animateScale': True, 'animateRotate': True}}}
        self.assertEqual(arguments, expected_config)
