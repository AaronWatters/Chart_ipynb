import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from chart_ipynb import chart_framework

class TestChartFramework(unittest.TestCase):

    @patch("chart_ipynb.chart_framework.load_requirements")
    def test_init(self, mock_load_requirements):
        widget = chart_framework.ChartSuperClass()
        assert mock_load_requirements.called
        mock_load_requirements.assert_called_with(widget)

        arguments = {}
        def mock_js_init(*args, **kwargs):
            arguments.update(kwargs)
        
        widget.js_init = mock_js_init
        config = {"test_attribute": 123}
        width = 122

        widget.initialize_chart(width, config)
        assert arguments["width"] == width
        
