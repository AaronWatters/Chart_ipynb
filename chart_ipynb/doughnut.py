
from . import chart_framework
from . import chart_setup
from . import utils

class Doughnut(chart_setup.Chart_init):

    title = "Doughnut chart"
    chart_type="doughnut"

    def __init__(self, options=None, title = None, *pargs, **kwargs):
        super(Doughnut, self).__init__(title = title, *pargs, **kwargs)
        if options is None:
            options = self.default_options()
        self.options = options
        self.reset()
    

def example():
    result = Doughnut()
    result.set_title("Chocolate Frosted")
    result.add("Big", 10, "brown")
    result.add("Medium", 7, "pink")
    result.add("Small", 3, "purple")
    result.setup()
    return result
