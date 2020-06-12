
import numpy as np

def clean_dict(**kwargs):
    "Like dict but with no None values make some values JSON serializable"
    # XXXX this should move to jp_proxy_widgets
    result = {}
    for kw in kwargs:
        v = kwargs[kw]
        if v is not None:
            if isinstance(v, np.ndarray):
                # listiffy arrays -- maybe should be done elsewhere
                v = v.tolist()
            if isinstance(v, np.floating):
                v = float(v)
            if type(v) is tuple:
                v = list(v)
            result[kw] = v
    return result

def options(
        responsive=True,
        legend=None,
        title=None,
        animation=None,
        **other_arguments
    ):
    return clean_dict(
        responsive=responsive,
        legend=legend,
        title=title,
        animation=animation,
        **other_arguments
    )

def config(
        type,
        data,
        options=None,
        **other_arguments,
    ):
    if options is None:
        options = {}
    return clean_dict(
        type=type,
        data=data,
        options=options,
        **other_arguments,
    )

def data(
        datasets,
        labels=None,
        **other_arguments
    ):
    return clean_dict(
        datasets=datasets,
        labels=labels,
        **other_arguments
    )

def dataset(
        data,
        label=None,
        backgroundColor=None, 
        **other_arguments
    ):
    return clean_dict(
        data=data,
        label=label,
        backgroundColor=backgroundColor,
        **other_arguments,
    )
