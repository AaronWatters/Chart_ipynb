

"""
Framework for wrapping Chart.js https://www.chartjs.org/ charts
as jupyter widgets.
"""

from . import local_files
from . import utils
import jp_proxy_widget
from IPython.display import display

required_javascript_modules = [
    local_files.vendor_path("js/Chart.js"),
]

def load_requirements(widget=None, silent=True, additional=()):
    """
    Load Javascript prerequisites into the notebook page context.
    """
    if widget is None:
        widget = jp_proxy_widget.JSProxyWidget()
        silent = False
    # Make sure jQuery and jQueryUI are loaded.
    widget.check_jquery()
    # load additional jQuery plugin code.
    all_requirements = list(required_javascript_modules) + list(additional)
    widget.load_js_files(all_requirements)
    if not silent:
        widget.element.html("<div>Requirements for <b>chart_ipynb</b> have been loaded.</div>")
        display(widget)

class ChartSuperClass(jp_proxy_widget.JSProxyWidget):

    title = "Chart.js"

    def __init__(self, *pargs, **kwargs):
        super(ChartSuperClass, self).__init__(*pargs, **kwargs)
        load_requirements(self)
        self.element.html("Uninitialized Chart.js widget.")
        self.clicked_info = []

    def initialize_chart(self, width, config):

        self.js_init("""
            element.empty();
            element.width(width);

            var canvas = $("<canvas></canvas>").appendTo(element);
            var ctx = canvas[0].getContext('2d');
            var chart = new Chart(ctx, config);
            element.chart_info = {
                chart: chart,
                canvas: canvas,
                context: ctx,
            };
            element.chart_info.get_pixels = function () {
                debugger;
                var cv = element.chart_info.canvas[0];
                var imgData = element.chart_info.context.getImageData(0, 0, cv.width, cv.height);
                return {"data": imgData.data, "height": imgData.height, "width": imgData.width};
            };
        """, width=width, config=config)

    def print_info(self, info):
        self.clicked_info.append(info)
        # print(info)

    def click_callback(self, callback=None):

        self.js_init("""
            var canvas = element.chart_info.canvas;
            var chart = element.chart_info.chart;
            var canvas0 = canvas[0];
            canvas0.onclick = function(event) {
                var info = {};
                console.log("onclick called" + event);
                var data = chart.getElementAtEvent(event);
                
                console.log(data[0]);
                var index = data[0]._index;
                var dataset_index = data[0]._datasetIndex;
                info.dataIndex = index;
                info.datasetIndex = dataset_index;

                var model = data[0]._model;
                info.backgroundColor = model.backgroundColor;
                info.borderColor = model.borderColor;
                
                var chart_info = data[0]._chart;
                var chart_config = chart_info.config;
                var dataset = chart_config.data.datasets[dataset_index];
                info.datasetLabel = dataset.label;
                info.label = chart_config.data.labels[index];
                info.dataValue = dataset.data[index];
                print_info(info);
                click_call(info);
            };
        """, click_call = callback, print_info=self.print_info)

    def off_click_event(self):
        self.js_init("""
            var canvas = element.chart_info.canvas;
            var chart = element.chart_info.chart;
            var canvas0 = canvas[0];
            canvas0.onclick = function(event) {
                // do nothing
            };
        """)

    def pixels_array(self):
        import numpy as np
        from jp_proxy_widget.hex_codec import hex_to_bytearray
        imgData = self.element.chart_info.get_pixels().sync_value()
        data_hex = imgData["data"]
        width = imgData["width"]
        height = imgData["height"]
        data_bytes = hex_to_bytearray(data_hex)
        bytes_per_pixel = 4
        array1d = np.array(data_bytes, dtype=np.ubyte)
        img_array = array1d.reshape((height, width, bytes_per_pixel))
        return img_array

    def pil_image(self):
        from PIL import Image
        return Image.fromarray(self.pixels_array(), mode="RGBA")

    def embed_image(self):
        from IPython.display import display
        display(self.pil_image())

    def save_image(self, to_path):
        im = self.pil_image()
        im.save(to_path)

    def default_options(self):
        true = True
        options = utils.options(
            responsive=true,
            legend=dict(position="top"),
            title=dict(display=true, text=self.title),
            animation=dict(animateScale=true, animateRotate=true)
        )
        self.options = options
        return options

    def set_title(self, title):
        self.options["title"]["text"] = title

    def config_json(self, config):
        import json
        return json.dumps(config)

    def html_script(self, chart):
        input_config = self.config_json(chart.config)
        html_chart = """
            <head>
            <title>Line Chart</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.min.js"></script>
            </head>

            <body>
                <canvas id="myChart" width="800" height="500"></canvas>
                <script>
                    var ctx = document.getElementById('myChart');
                    var myChart = new Chart(ctx, %s);
                </script>
            </body>
        """%(input_config)
        return html_chart

def example_donut():
    "just a test."
    chartColors = dict(
        red= 'rgb(255, 99, 132)',
        orange= 'rgb(255, 159, 64)',
        yellow= 'rgb(255, 205, 86)',
        green= 'rgb(75, 192, 192)',
        blue= 'rgb(54, 162, 235)',
        purple= 'rgb(153, 102, 255)',
        grey= 'rgb(201, 203, 207)'
    )

    import random

    def randomScalingFactor():
        return round(random.random() * 200)

    ndata = 6

    data = [randomScalingFactor() for i in range(ndata)]
    names_and_colors = list(chartColors.items())[:ndata]
    colors = [nc[1] for nc in names_and_colors]
    names = [nc[0] for nc in names_and_colors]
    true=True # convenience

    config = utils.config(
        type="doughnut",
        data= utils.data(
            datasets = [
                utils.dataset(
                    label="My Dataset",
                    data=data,
                    backgroundColor=colors,
                )
            ],
            labels=names
        ),
        options= utils.options(
            responsive=true,
            legend=dict(position="top"),
            title=dict(display=true, text="Tasty Donuts"),
            animation=dict(animateScale=true, animateRotate=true)
        ),
    )
    result = ChartSuperClass()
    result.initialize_chart(width=800, config=config)
    return result
    