import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from chart_ipynb import chart_framework, utils, bubble
import jp_proxy_widget

class TestBubble(unittest.TestCase):

    @patch("chart_ipynb.chart_framework.load_requirements")
    @patch("chart_ipynb.utils.options")
    def test_init(self, mock_load_requirements, mock_options):
        widget = bubble.Bubble()
        assert mock_load_requirements.called
        assert mock_options.called
        assert widget.title == 'Bubble Chart'
        assert widget.chart_type == 'bubble'