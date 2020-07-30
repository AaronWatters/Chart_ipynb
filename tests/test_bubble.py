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

    @patch("chart_ipynb.bubble.Bubble")
    def test_scatter_chart(self, mock_bubble):
        import pandas as pd
        d1 = pd.DataFrame({'x':[1,3,5],'y':[1,3,5]})
        d2 = [{'x':1,'y':1},{'x':3,'y':3},{'x':5,'y':5}]
        d3 = {'x':[1,3,5],'y':[1,3,5]}
        d4 = {'dataset1':[{'x':1,'y':1},{'x':3,'y':3},{'x':5,'y':5}]}
        bubble.bubble_chart('t',d1,'x','y')
        bubble.bubble_chart('t',d2)
        bubble.bubble_chart('t',d3)
        bubble.bubble_chart('t',d4)
        assert mock_bubble.called