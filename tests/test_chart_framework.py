import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from chart_ipynb import chart_framework
import jp_proxy_widget

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

    @patch("chart_ipynb.chart_framework.ChartSuperClass")
    @patch("chart_ipynb.utils.options")
    def test_example_donut(self, mock_chart_superclass, mock_options):
        chart_framework.example_donut()
        assert mock_options.called

    @patch("jp_proxy_widget.JSProxyWidget")
    def test_load_requirements(self, mock_proxy_widget):
        import jp_proxy_widget
        widgets = []
        def proxy_widget():
            result = MagicMock()
            #result.check_jquery = MagicMock()
            widgets.append(result)
            return result
        jp_proxy_widget.JSProxyWidget = proxy_widget
        # call load requirements using mock proxy widget
        chart_framework.load_requirements()
        mock_proxy_widget.some_other_method = MagicMock()
        mock_proxy_widget.check_jquery = MagicMock()
        assert not mock_proxy_widget.some_other_method.called
        assert widgets[0].check_jquery.called
        assert widgets[0].load_js_files.called
        assert not widgets[0].some_other_method.called

    @patch("jp_proxy_widget.JSProxyWidget")
    def test_default_options(self, mock_proxy_widget):
        widget = chart_framework.ChartSuperClass()
        options = widget.default_options()
        expected_options = {
                'animation': {'animateRotate': True, 'animateScale': True},
                'legend': {'position': 'top'},
                'responsive': True,
                'title': {'display': True, 'text': 'Chart.js'},
                #"bogux": "this is wrong",
             }
        self.assertEqual(options, expected_options)

    @patch("jp_proxy_widget.JSProxyWidget")
    def test_set_title(self, mock_proxy_widge):
        widget = chart_framework.ChartSuperClass()
        options = widget.default_options()
        widget.set_title('test')
        # widget.initialize_chart(width=800, config=config)
        title = widget.options['title']['text']
        self.assertEqual(title, 'test')
    
    @patch("jp_proxy_widget.JSProxyWidget")
    def test_callback(self, mock_proxy_widget):
        '''
        not implement yet
        '''

    @patch("jp_proxy_widget.JSProxyWidget")
    @patch("chart_ipynb.chart_framework.example_donut")
    def test_pixels_array(self, mock_proxy_widge, mock_donut):
        widget = mock_donut()
        widget.save_image('tests.png')
        assert mock_donut.called
        # assert mock_proxy_widge.called