from setuptools import setup

url = ""
version = "0.1.0"
readme = open('README.md').read()

setup(
    name="chart_ipynb",
    packages=["chart_ipynb"],
    version=version,
    description="Simple jupyter widget wrappers for Chart.js chart types",
    long_description=readme,
    include_package_data=True,
    author="Aaron Watters",
    author_email="awatters@flatironinstitute.org",
    url=url,
    install_requires=[
        "jp_proxy_widget", 
        "datetime", 
        "numpy", 
        "pandas",
        "pandas_datareader", 
        "pillow", 
        "imageio",
        "jupyter-ui-poll",
        "pytz",
        ],
    license="MIT"
)
