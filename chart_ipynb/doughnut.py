
from . import chart_framework
from . import utils

class Doughnut(chart_framework.ChartSuperClass):

    title = "Doughnut chart"

    def __init__(self, options=None, *pargs, **kwargs):
        super(Doughnut, self).__init__(*pargs, **kwargs)
        if options is None:
            options = self.default_options()
        self.options = options
        self.labels = []
        self.data = []
        self.colors = []
    
    def add(self, label, datum, color):
        self.labels.append(label)
        self.data.append(datum)
        self.colors.append(color)

    def setup(self, width=800):
        config = utils.config(
            type="doughnut",
            data=utils.data(
                datasets=[
                    utils.dataset(
                        label="My dataset",
                        data=self.data,
                        backgroundColor=self.colors
                    )
                ],
                labels = self.labels,
            ),
            options=self.options,
        )
        self.initialize_chart(width, config)

def example():
    result = Doughnut()
    result.set_title("Chocolate Frosted")
    result.add("Big", 10, "brown")
    result.add("Medium", 7, "pink")
    result.add("Small", 3, "purple")
    result.setup()
    return result
