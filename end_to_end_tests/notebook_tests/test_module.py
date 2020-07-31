
# Put the widget inside a module so we can hide the test string from the notebook source

import chart_ipynb
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
    result = "print out sth"
#     result.value = test_string
    display(result)
    display(test_string)
