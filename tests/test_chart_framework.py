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
    
    def test_callback(self):
        widget = chart_framework.ChartSuperClass()
        arguments = []
        def print_info():
            arguments.append('nothing')
        widget.print_info = print_info
        widget.click_callback()
        assert not arguments
        assert not widget.clicked_info

    def test_off_click(self):
        widget = chart_framework.ChartSuperClass()
        arguments = {}
        def js_init(evt):
            arguments['off']=True
        widget.js_init = js_init
        widget.off_click_event()
        assert arguments['off']

    @patch("jp_proxy_widget.JSProxyWidget")
    def test_pixels_array(self,mock_proxy_widget):
        import numpy as np
        widget = chart_framework.ChartSuperClass()
        widget.element = MagicMock()
        widget.element.chart_info = MagicMock()
        class dummy:
            def sync_value(self):
                return {'data':'07070707',
                        'width': 1,
                        'height': 1}
        def get_pixels():
            return dummy()
        widget.element.chart_info.get_pixels = get_pixels
        img_arr = widget.pixels_array()
        assert isinstance(img_arr, np.ndarray)
        self.assertEqual(img_arr.tolist(), [[[7,7,7,7]]])

    def test_embed_image(self):
        widget = chart_framework.ChartSuperClass()
        def pixels_array():
            import numpy as np
            return np.ones((10,15,3))
        widget.pixels_array = pixels_array
        widget.embed_image()

    def test_save_image(self):
        import numpy as np
        widget = chart_framework.ChartSuperClass()
        def pixels_array():
            return np.ones((10,15,3))
        widget.pixels_array = pixels_array
        import tempfile
        file = tempfile.NamedTemporaryFile(suffix='.png')
        widget.save_image(file)
        response = {}
        with open(file.name, 'rb') as f:
            data = {'image': f}
            response.update(data)
        assert response['image']
        