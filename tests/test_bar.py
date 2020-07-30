import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from chart_ipynb import chart_framework, utils, bar
import jp_proxy_widget

class TestBar(unittest.TestCase):

    @patch("chart_ipynb.chart_framework.load_requirements")
    @patch("chart_ipynb.utils.options")
    def test_init(self, mock_load_requirements, mock_options):
        widget = bar.Bar()
        assert mock_load_requirements.called
        assert mock_options.called
        assert widget.title == 'Bar Chart'
        assert widget.chart_type == 'bar'

    @patch("chart_ipynb.bar.Bar")
    def test_line_chart(self,mock_bar):
        import pandas as pd
        bar.bar_chart('test',{'t1':1,'t2':2})
        df = pd.DataFrame({'t':['t1','t2'],'v':[1,1]})
        bar.bar_chart('test',df, 't','v')
        bar.bar_chart('test',{'label':['t1','t2'],'dataset1':[1,1]})
        assert mock_bar.called