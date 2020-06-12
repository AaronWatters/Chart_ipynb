
from . import local_files
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

    def __init__(self, *pargs, **kwargs):
        super(ChartSuperClass, self).__init__(*pargs, **kwargs)
        load_requirements(self)
        self.element.html("Uninitialized Chart.js widget.")

    def initialize_chart(self, width, config):
        self.js_init("""
            element.empty();
            element.width(width);

            var canvas = $("<canvas></canvas>").appendTo(element);
            var ctx = canvas[0].getContext('2d');
            element.myDoughnut = new Chart(ctx, config);
        """, width=width, config=config)

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

    config = dict(
        type="doughnut",
        data= dict(
            datasets = [
                dict(
                    label="My Dataset",
                    data=data,
                    backgroundColor=colors,
                )
            ],
            labels=names
        ),
        options= dict(
            responsive=true,
            legend=dict(position="top"),
            title=dict(display=true, text="Dunkin Donut"),
            animation=dict(animateScale=true, animateRotate=true)
        ),
    )
    result = ChartSuperClass()
    result.initialize_chart(width=800, config=config)
    return result
    