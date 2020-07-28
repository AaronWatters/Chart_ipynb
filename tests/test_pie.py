import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from chart_ipynb import chart_framework, utils, pie
import jp_proxy_widget

class TestPie(unittest.TestCase):

    @patch("chart_ipynb.chart_framework.load_requirements")
    @patch("chart_ipynb.utils.options")
    def test_init(self, mock_load_requirements, mock_options):
        widget = pie.Pie()
        assert mock_load_requirements.called
        assert mock_options.called
        assert widget.title == 'Pie Chart'
        assert widget.chart_type == 'pie'