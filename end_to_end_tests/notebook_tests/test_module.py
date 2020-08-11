
# Put the widget inside a module so we can hide the test string from the notebook source

import chart_ipynb
from chart_ipynb import chart_framework
from IPython.display import display
import ipywidgets as widgets

secret_label = "SECRET BUTTON LABEL"

def get_a_button():
    b = widgets.Button(
        description=secret_label,
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Click me',
        icon='check'
    )
    display(b)

test_string = "THIS IS THE SECRET TEST STRING"

def get_a_widget():
    widget = chart_framework.example_donut()
    display(test_string)
    display(widget)
