

"""
Framework for wrapping Chart.js https://www.chartjs.org/ charts
as jupyter widgets.
"""

from . import local_files
from . import utils
import jp_proxy_widget

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

    def initialize_chart(self, width, config):

        def print_info(info):
            print(info)

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
            var canvas0 = canvas[0];
            canvas0.onclick = function(event) {
                debugger;
                console.log("onclick called" + event);
                var data = chart.getElementAtEvent(event);
                console.log(data[0]);
                //var index = data[0]._index;
                //console.log("index = " + index);
                var chart_info = data[0]._chart;
                print_info(data[0]._index)
            }
        """, width=width, config=config, print_info = print_info)
    

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
    